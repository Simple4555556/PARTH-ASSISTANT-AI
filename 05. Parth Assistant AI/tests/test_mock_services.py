"""
PARTH ASSISTANT AI — Mock School ERP Services Test Suite (Phase 2)
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


def test_get_student_profile():
    token = get_token("student1")
    res = client.get("/api/mock/students/S101", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["student_id"] == "S101"
    assert "Aarav" in data["student_name"]


def test_get_parent_children_and_attendance():
    token = get_token("parent1")
    # Children lookup
    res_children = client.get("/api/mock/children/P201", headers={"Authorization": f"Bearer {token}"})
    assert res_children.status_code == 200
    children = res_children.json()
    assert len(children) >= 1
    assert children[0]["student_id"] == "S101"

    # Attendance lookup
    res_att = client.get("/api/mock/students/S101/attendance", headers={"Authorization": f"Bearer {token}"})
    assert res_att.status_code == 200
    assert res_att.json()["overall_percentage"] >= 85.0


def test_recent_attendance_logs():
    token = get_token("student1")
    res = client.get("/api/mock/students/S101/attendance/recent?limit=3", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    logs = res.json()
    assert isinstance(logs, list)
    assert len(logs) <= 3


def test_teacher_mark_attendance_and_recalculation():
    token = get_token("teacher1")
    payload = {
        "student_id": "S101",
        "date": "2026-08-20",
        "status": "PRESENT",
        "subject": "Mathematics",
        "remarks": "On-time participation"
    }
    res = client.post("/api/mock/attendance/mark", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["status"] == "PRESENT"


def test_principal_class_analytics():
    token = get_token("principal1")
    res = client.get("/api/mock/analytics/class/10-A", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["attendance_rate"] == 93.5


def test_support_call_request_workflow():
    token = get_token("parent1")
    req_payload = {
        "parent_id": "P201",
        "student_id": "S101",
        "teacher_id": "T301",
        "reason": "Discuss recent Math evaluation"
    }
    res = client.post("/api/mock/support/call-request", json=req_payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUBMITTED"
    req_id = data["request_id"]

    # Retrieve request
    get_res = client.get(f"/api/mock/support/request/{req_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_res.status_code == 200
    assert get_res.json()["reason"] == "Discuss recent Math evaluation"


def test_get_teacher_details():
    token = get_token("parent1")
    res = client.get("/api/mock/teachers/T301", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["name"] == "Sunita Verma"
