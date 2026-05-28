# day05/app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import asyncio
import os
import traceback
from code_review_agent import run_code_review

load_dotenv()

app = Flask(__name__)


# ══════════════════════════════════════════════════════
# HEALTH CHECK
# Render and every deployment platform hits this to
# confirm the server is alive. Always include this.
# ══════════════════════════════════════════════════════

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "AI Code Review Agent",
        "version": "1.0.0"
    }), 200


# ══════════════════════════════════════════════════════
# MAIN ENDPOINT — POST /review
#
# Accepts:
#   { "source": "path/to/file.py" }
#   { "source": "https://github.com/user/repo/blob/main/file.py" }
#
# Returns:
#   { "success": true, "report": "...", "report_file": "..." }
# ══════════════════════════════════════════════════════

@app.route("/review", methods=["POST"])
def review():
    # ── Validate input ─────────────────────────────────
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body must be JSON"
        }), 400

    source = data.get("source", "").strip()

    if not source:
        return jsonify({
            "success": False,
            "error": "Missing required field: source"
        }), 400

    # Validate source — must be a URL or .py file
    is_url = source.startswith("http")
    is_python = source.endswith(".py")

    if not is_url and not is_python:
        return jsonify({
            "success": False,
            "error": "Source must be a GitHub URL or a .py file path"
        }), 400

    # ── Run the agent pipeline ─────────────────────────
    try:
        print(f"\n[API] Review requested for: {source}")

        # asyncio.run() runs the async agent from sync Flask
        report = asyncio.run(run_code_review(source))

        if not report:
            return jsonify({
                "success": False,
                "error": "Agent failed to generate report"
            }), 500

        return jsonify({
            "success": True,
            "source": source,
            "report": report
        }), 200

    except FileNotFoundError:
        return jsonify({
            "success": False,
            "error": f"File not found: {source}"
        }), 404

    except Exception as e:
        print(f"[API] Error: {traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ══════════════════════════════════════════════════════
# ERROR HANDLERS
# Clean JSON errors instead of HTML Flask defaults
# ══════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"success": False, "error": "Method not allowed"}), 405


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n AI Code Review Agent API")
    print(f" Running on http://localhost:{port}")
    print(f" Endpoints:")
    print(f"   GET  /health")
    print(f"   POST /review")
    app.run(host="0.0.0.0", port=port, debug=False)