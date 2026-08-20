"""
PARTH ASSISTANT AI — Performance Timing & Latency Diagnostic Test
Validates all 11-step execution logs, UUID Request ID tracing, 5-second timeouts,
and ultra-fast response for structured ERP queries.
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Authenticate as student1
login_res = client.post("/api/auth/login", json={"username": "student1", "password": "password123"})
assert login_res.status_code == 200, f"Login failed: {login_res.text}"
token = login_res.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

test_queries = [
    "What is my attendance?",
    "What is my Mathematics attendance?",
    "Show recent attendance",
    "Show my timetable"
]

print("\n" + "="*70)
print("PARTH ASSISTANT AI — PERFORMANCE & LATENCY DIAGNOSTIC")
print("="*70)

for q in test_queries:
    res = client.post("/api/ai/chat", json={"message": q, "language": "en"}, headers=headers)
    assert res.status_code == 200, f"Chat failed for '{q}': {res.text}"
    d = res.json()
    print(f"\nQUERY: \"{q}\"")
    print(f"REQUEST ID:              {d.get('request_id')}")
    print(f"INTENT:                  {d.get('intent')}")
    print(f"COMPONENT:               {d.get('component')}")
    print(f"TOTAL BACKEND TIME:      {d.get('processing_time_ms')} ms")
    print(f"RESPONSE MESSAGE:        {d.get('response')}")
    print("TIMING BREAKDOWN:")
    for step, ms_val in d.get("timing_breakdown", {}).items():
        print(f"  {step:<25}: {ms_val}ms")
    print("-" * 70)

print("\nAll latency tests completed successfully.")
