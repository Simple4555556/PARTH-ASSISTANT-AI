"""
PARTH ASSISTANT AI — Conversational-First UX Acceptance & Security Test Suite
Verifies all 8 Acceptance Tests specified in Section 23 of UX Override Specification.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def get_token(username: str) -> str:
    res = client.post("/api/auth/login", json={"username": username, "password": "password123"})
    return res.json()["access_token"]


# ==========================================
# ACCEPTANCE TESTS (SECTION 23)
# ==========================================

def test_acceptance_1_student_login_conversational_first():
    """TEST 1: Login as Student -> Returns token for session initialization."""
    token = get_token("student1")
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "STUDENT"
    assert "Aarav" in data["name"]


def test_acceptance_2_student_own_attendance_component():
    """TEST 2: Student asks 'What is my attendance?' -> Returns ONLY attendance card component."""
    token = get_token("student1")
    res = client.post(
        "/api/ai/chat",
        json={"message": "What is my attendance?", "conversation_id": "TEST-CONV-ATT-1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "STUDENT"
    assert data["intent"] == "VIEW_OWN_ATTENDANCE"
    assert data["ui_action"] == "SHOW_COMPONENT"
    assert data["component"] == "attendance-card"
    assert "overall_percentage" in data["data"]


def test_acceptance_3_parent_child_attendance_component():
    """TEST 3: Parent asks 'How much attendance does my child have?' -> Returns ONLY child attendance component."""
    token = get_token("parent1")
    res = client.post(
        "/api/ai/chat",
        json={"message": "How much attendance does my child have?", "conversation_id": "TEST-CONV-ATT-2"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "PARENT"
    assert data["intent"] == "VIEW_CHILD_ATTENDANCE"
    assert data["ui_action"] == "SHOW_COMPONENT"
    assert data["component"] == "attendance-card"
    assert "Rahul" in data["message"] or "Rahul" in str(data["data"])


def test_acceptance_4_teacher_mark_attendance_action_ui():
    """TEST 4: Teacher asks 'Mark Rahul absent.' -> Returns Attendance action component."""
    token = get_token("teacher1")
    res = client.post(
        "/api/ai/chat",
        json={"message": "Mark Rahul absent.", "conversation_id": "TEST-CONV-MARK-1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "TEACHER"
    assert data["intent"] == "MARK_ATTENDANCE"
    assert data["component"] == "mark-attendance"
    assert "Rahul" in data["data"]["student_name"]
    assert data["data"]["status"] == "ABSENT"



def test_acceptance_5_principal_overall_attendance_analytics():
    """TEST 5: Principal asks 'What is the overall attendance?' -> Returns Analytics component only."""
    token = get_token("principal1")
    res = client.post(
        "/api/ai/chat",
        json={"message": "What is the overall attendance?", "conversation_id": "TEST-CONV-ANALYTICS-1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "PRINCIPAL"
    assert data["intent"] == "VIEW_SCHOOL_ANALYTICS"
    assert data["ui_action"] == "SHOW_CHART"
    assert data["component"] == "attendance-analytics"
    assert "overall_attendance" in data["data"]


def test_acceptance_6_authorized_principal_database_view():
    """TEST 6: Authorized user (Principal) asks 'Show me the database.' -> Returns Database component."""
    token = get_token("principal1")
    res = client.post(
        "/api/ai/chat",
        json={"message": "Show me the database.", "conversation_id": "TEST-CONV-DB-1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "PRINCIPAL"
    assert data["intent"] in ["DATABASE_ACCESS", "VIEW_DATABASE"]
    assert data["ui_action"] == "OPEN_PAGE"
    assert data["component"] == "database-view"
    assert "collections" in data["data"]
    # Verify no secrets exposed
    raw_str = str(data)
    assert "password" not in raw_str.lower()
    assert "secret" not in raw_str.lower()
    assert "api_key" not in raw_str.lower()


def test_acceptance_7_unauthorized_database_access_denied():
    """TEST 7: Unauthorized user (Student/Parent) asks 'Show me the database.' -> Access denied."""
    for username, role in [("student1", "STUDENT"), ("parent1", "PARENT")]:
        token = get_token(username)
        res = client.post(
            "/api/ai/chat",
            json={"message": "Show me the database.", "conversation_id": f"TEST-CONV-DB-DENIED-{role}"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 200
        data = res.json()
        assert data["role"] == role
        assert data["ui_action"] == "NONE"
        assert data["component"] is None
        assert "don't have permission" in data["message"].lower() or "sorry" in data["message"].lower()



def test_acceptance_8_user_open_complete_dashboard():
    """TEST 8: User asks 'Open complete dashboard.' -> Returns Full dashboard component."""
    token = get_token("student1")
    res = client.post(
        "/api/ai/chat",
        json={"message": "Open complete dashboard.", "conversation_id": "TEST-CONV-DASH-1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "OPEN_DASHBOARD"
    assert data["ui_action"] == "OPEN_PAGE"
    assert data["component"] == "full-dashboard"
