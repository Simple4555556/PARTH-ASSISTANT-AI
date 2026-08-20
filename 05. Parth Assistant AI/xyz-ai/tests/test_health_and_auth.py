import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "PARTH ASSISTANT AI"


def test_student_login_and_me():
    # Login as Student
    login_res = client.post("/api/auth/login", json={"username": "student1", "password": "password123"})
    assert login_res.status_code == 200
    data = login_res.json()
    assert data["role"] == "STUDENT"
    assert data["user_id"] == "S101"
    token = data["access_token"]

    # Access /me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert "Aarav" in me_res.json()["name"]


def test_parent_login_and_child_access():
    login_res = client.post("/api/auth/login", json={"username": "parent1", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # Allowed child access
    child_res = client.get("/api/mock/students/S101/attendance", headers={"Authorization": f"Bearer {token}"})
    assert child_res.status_code == 200
    assert child_res.json()["overall_percentage"] > 80.0


    # Forbidden unrelated child access
    forbidden_res = client.get("/api/mock/students/S103/attendance", headers={"Authorization": f"Bearer {token}"})
    assert forbidden_res.status_code == 403


def test_teacher_login_and_attendance_mark():
    login_res = client.post("/api/auth/login", json={"username": "teacher1", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # Mark attendance for assigned class student S101 (10-A)
    mark_payload = {
        "student_id": "S101",
        "date": "2026-08-19",
        "status": "ABSENT",
        "subject": "Mathematics",
        "remarks": "Medical leave test"
    }
    mark_res = client.post("/api/mock/attendance/mark", json=mark_payload, headers={"Authorization": f"Bearer {token}"})
    assert mark_res.status_code == 200
    assert mark_res.json()["success"] is True


def test_principal_login_and_analytics():
    login_res = client.post("/api/auth/login", json={"username": "principal1", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # Access school analytics
    analytics_res = client.get("/api/mock/analytics/attendance", headers={"Authorization": f"Bearer {token}"})
    assert analytics_res.status_code == 200
    assert analytics_res.json()["overall_attendance"] == 92.4


def test_invalid_login():
    login_res = client.post("/api/auth/login", json={"username": "invalid_user", "password": "wrong_password"})
    assert login_res.status_code == 401
