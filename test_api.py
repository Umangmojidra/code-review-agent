# day05/test_api.py
import requests
import json

BASE_URL = "http://localhost:5000"

# Test 1: Health check
print("Testing /health...")
r = requests.get(f"{BASE_URL}/health")
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}\n")

# Test 2: Review local file
print("Testing /review...")
r = requests.post(
    f"{BASE_URL}/review",
    json={"source": "E:/AI-Agents-Journey/day05_Project/sample_code.py"}
)
print(f"Status: {r.status_code}")
data = r.json()
print(f"Success: {data['success']}")
if data['success']:
    print(f"Report length: {len(data['report'])} chars")
    print(f"\nFirst 500 chars of report:\n{data['report'][:500]}")
else:
    print(f"Error: {data['error']}")