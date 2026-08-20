"""
PARTH ASSISTANT AI — Authentication, Registration & Session Security Tests
Validates:
- Student, Parent, Teacher Registration & Password Hashing
- Principal Public Registration Block (403 Forbidden)
- Role verification & Ownership checks
- Logout & Token Revocation
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


import uuid

def test_student_registration_and_login():
    username = f"new_student_{uuid.uuid4().hex[:6]}"
    reg_payload = {
        "username": username,
        "name": "New Student",
        "email": f"{username}@school.edu",
        "password": "securepassword123",
        "confirm_password": "securepassword123",
        "grade_section": "10-A"
    }
    res = client.post("/api/auth/register/student", json=reg_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["role"] == "STUDENT"

    # Login with new credentials
    login_res = client.post("/api/auth/login", json={"username": username, "password": "securepassword123"})
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()


def test_student_registration_password_mismatch():
    res = client.post("/api/auth/register/student", json={
        "username": f"mismatch_{uuid.uuid4().hex[:6]}",
        "name": "Mismatch",
        "email": "mismatch@school.edu",
        "password": "password123",
        "confirm_password": "wrongpassword"
    })
    assert res.status_code == 400
    assert "Passwords do not match" in res.json()["detail"]


def test_parent_registration_with_linked_child():
    username = f"new_parent_{uuid.uuid4().hex[:6]}"
    res = client.post("/api/auth/register/parent", json={
        "username": username,
        "name": "New Parent",
        "email": f"{username}@gmail.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123",
        "linked_student_id": "S101"
    })
    assert res.status_code == 200
    assert res.json()["role"] == "PARENT"


def test_parent_registration_invalid_child():
    res = client.post("/api/auth/register/parent", json={
        "username": f"bad_parent_{uuid.uuid4().hex[:6]}",
        "name": "Bad Parent",
        "email": "bad@gmail.com",
        "password": "password123",
        "confirm_password": "password123",
        "linked_student_id": "S9999_NON_EXISTENT"
    })
    assert res.status_code == 404
    assert "not found" in res.json()["detail"]


def test_teacher_registration_requires_verification_code():
    username = f"new_teacher_{uuid.uuid4().hex[:6]}"
    # Valid code
    res = client.post("/api/auth/register/teacher", json={
        "username": username,
        "name": "New Teacher",
        "email": f"{username}@school.edu",
        "password": "password123",
        "confirm_password": "password123",
        "subject": "Physics",
        "verification_code": "TEACHER2026"
    })
    assert res.status_code == 200
    assert res.json()["role"] == "TEACHER"

    # Invalid code
    res_bad = client.post("/api/auth/register/teacher", json={
        "username": "fake_teacher",
        "name": "Fake Teacher",
        "email": "fake@school.edu",
        "password": "password123",
        "confirm_password": "password123",
        "subject": "Physics",
        "verification_code": "INVALID_CODE"
    })
    assert res_bad.status_code == 403
    assert "Invalid teacher authorization code" in res_bad.json()["detail"]


def test_principal_public_registration_is_strictly_forbidden():
    res = client.post("/api/auth/register/principal")
    assert res.status_code == 403
    assert "cannot be registered publicly" in res.json()["detail"]


def test_logout_revokes_session_token():
    # 1. Login
    login_res = client.post("/api/auth/login", json={"username": "student1", "password": "password123"})
    token = login_res.json()["access_token"]

    # 2. Verify token works
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200

    # 3. Logout
    logout_res = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_res.status_code == 200

    # 4. Verify token is now rejected
    me_after_logout = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_after_logout.status_code == 401
    assert "revoked" in me_after_logout.json()["detail"]
