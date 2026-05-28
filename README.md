# AI Code Review Agent 🤖

A production-grade multi-agent system that performs automated code reviews using Claude AI.

The system analyses Python code for:

* 🐛 Bugs
* ⚠️ Code quality issues
* 🔒 Security vulnerabilities

using a coordinator-subagent architecture with parallel AI agents.

---

# Architecture

```text
POST /review (source)
        ↓
   COORDINATOR
        ↓
Sequential:
Code Fetcher (MCP filesystem / fetch)
        ↓
Parallel via asyncio.gather():

Bug Detective ────┐
Quality Reviewer ─┤
Security Scanner ─┘

        ↓
Sequential:
Report Writer → Markdown Report
        ↓
JSON Response
```

---

# Features

* Multi-agent architecture with specialised Claude agents
* Parallel code analysis using `asyncio.gather()`
* MCP integration for local files and GitHub URLs
* Structured markdown reports with severity ratings
* REST API built with Flask
* Dockerised production-ready deployment
* Render cloud deployment support

---

# API Endpoints

## Health Check

```http
GET /health
```

---

## Review Code

```http
POST /review
Content-Type: application/json
```

### Request

```json
{
  "source": "/path/to/file.py"
}
```

or

```json
{
  "source": "https://github.com/user/repo/blob/main/file.py"
}
```

---

## Response

```json
{
  "success": true,
  "source": "sample_code.py",
  "report": "# Code Review Report..."
}
```

---

# Tech Stack

* **Claude API (claude-sonnet-4-6)** — AI analysis engine
* **MCP (Model Context Protocol)** — Filesystem + fetch servers
* **Flask** — REST API framework
* **asyncio** — Parallel execution
* **Docker** — Containerisation
* **Render** — Cloud deployment

---

# Local Setup

```bash
git clone https://github.com/Umangmojidra/code-review-agent.git

cd code-review-agent

pip install -r requirements.txt

npm install -g @modelcontextprotocol/server-filesystem

cp .env.example .env
# Add your ANTHROPIC_API_KEY

python app.py
```

---

# Sample Report Output

The generated report includes:

* 🐛 Bug findings with severity levels
* ⚠️ Code quality improvements
* 🔒 Security vulnerability analysis
* ✅ Top priority fixes
* 📊 Overall review summary

---

# Live Demo

```text
https://ai-code-review-agent.onrender.com
```

---

# Future Improvements

* Multi-language code support
* GitHub PR review integration
* CI/CD integration
* Persistent report storage
* Streaming responses

---

# License

MIT License
