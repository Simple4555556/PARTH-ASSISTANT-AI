"""
PARTH ASSISTANT AI — Backend Application Server
"""

import os
from typing import Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from .models import (
    LoginRequest, TokenResponse, UserProfile, UserRole,
    StudentRegisterRequest, ParentRegisterRequest, TeacherRegisterRequest, RegisterResponse,
    ChatMessageRequest, ChatMessageResponse, AttendanceMarkRequest,
    AttendanceMarkResponse, SupportCallRequest, SupportCallResponse
)
from .auth import authenticate_user, get_current_user, require_role, hash_password, revoke_token, security_scheme
from .router_mock_erp import router as mock_erp_router
from .router_chat import router as chat_router
from .router_voice import router as voice_router
from .mock_data import (
    MOCK_USERS, MOCK_STUDENTS, MOCK_ANALYTICS, MOCK_TEACHERS, MOCK_SUPPORT_REQUESTS
)
from database.db_engine import db
from fastapi.security import HTTPAuthorizationCredentials

app = FastAPI(
    title="PARTH ASSISTANT AI API",
    description="Human-Like AI School Assistant API for School ERP Ecosystem",
    version="2.0.0"
)

# Secure CORS for authorized frontend origins
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://parth-assistant-ai.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(mock_erp_router)
app.include_router(chat_router)
app.include_router(voice_router)


@app.get("/api/health", summary="Basic API Health Check")
def health_check():
    return {
        "status": "healthy",
        "service": "PARTH ASSISTANT AI",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "2.0.0",
        "ecosystem": "School ERP Ecosystem"
    }


# ==========================================
# AUTHENTICATION & REGISTRATION ENDPOINTS
# ==========================================

@app.post("/api/auth/login", response_model=TokenResponse, summary="User Login for All 4 Roles")
def login(login_data: LoginRequest):
    return authenticate_user(login_data)


@app.post("/api/auth/logout", summary="User Logout and Token Invalidation")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    revoke_token(credentials.credentials)
    return {"success": True, "message": "Successfully logged out. Session invalidated."}


@app.post("/api/auth/register/student", response_model=RegisterResponse, summary="Student Self-Registration")
def register_student(req: StudentRegisterRequest):
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    
    if db.get_user_by_username(req.username):
        raise HTTPException(status_code=409, detail=f"Username '{req.username}' is already registered.")

    student_id = req.student_id or f"S{len(db.users) + 101}"
    new_user = {
        "user_id": student_id,
        "username": req.username,
        "password_hash": hash_password(req.password),
        "role": "STUDENT",
        "name": req.name,
        "email": req.email,
        "grade_section": req.grade_section or "10-A"
    }
    db.create_user(new_user)
    return RegisterResponse(
        success=True,
        message="Student registration successful.",
        user_id=student_id,
        username=req.username,
        role=UserRole.STUDENT
    )


@app.post("/api/auth/register/parent", response_model=RegisterResponse, summary="Parent Self-Registration with Child Linking")
def register_parent(req: ParentRegisterRequest):
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    
    if db.get_user_by_username(req.username):
        raise HTTPException(status_code=409, detail=f"Username '{req.username}' is already registered.")

    # Validate linked student exists in mock database
    if not db.get_student(req.linked_student_id):
        raise HTTPException(status_code=404, detail=f"Student ID '{req.linked_student_id}' not found in school registry.")

    parent_id = f"P{len(db.users) + 201}"
    new_user = {
        "user_id": parent_id,
        "username": req.username,
        "password_hash": hash_password(req.password),
        "role": "PARENT",
        "name": req.name,
        "email": req.email,
        "child_ids": [req.linked_student_id]
    }
    db.create_user(new_user)
    return RegisterResponse(
        success=True,
        message="Parent registration successful.",
        user_id=parent_id,
        username=req.username,
        role=UserRole.PARENT
    )


@app.post("/api/auth/register/teacher", response_model=RegisterResponse, summary="Teacher Registration with Verification Code")
def register_teacher(req: TeacherRegisterRequest):
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    
    # Controlled teacher verification (Never trust raw frontend role claims)
    if req.verification_code != "TEACHER2026":
        raise HTTPException(
            status_code=403,
            detail="Invalid teacher authorization code. Staff verification required."
        )

    if db.get_user_by_username(req.username):
        raise HTTPException(status_code=409, detail=f"Username '{req.username}' is already registered.")

    teacher_id = f"T{len(db.users) + 301}"
    new_user = {
        "user_id": teacher_id,
        "username": req.username,
        "password_hash": hash_password(req.password),
        "role": "TEACHER",
        "name": req.name,
        "email": req.email,
        "assigned_classes": ["10-A", "10-B"],
        "subject": req.subject
    }
    db.create_user(new_user)
    return RegisterResponse(
        success=True,
        message="Teacher registration and verification successful.",
        user_id=teacher_id,
        username=req.username,
        role=UserRole.TEACHER
    )


@app.post("/api/auth/register/principal", summary="Principal Registration Attempt (Blocked)")
def register_principal():
    """Principal accounts cannot be created via public registration."""
    raise HTTPException(
        status_code=403,
        detail="Principal accounts cannot be registered publicly. Controlled administrative setup required."
    )


@app.get("/api/auth/me", summary="Get Current Authenticated User Profile")
def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "role": current_user["role"],
        "name": current_user["name"],
        "email": current_user["email"],
        "child_ids": current_user.get("child_ids"),
        "assigned_classes": current_user.get("assigned_classes")
    }



# ==========================================
# MOCK SCHOOL ERP ENDPOINTS
# ==========================================

@app.get("/api/mock/students/{student_id}", summary="Get Student Details")
def get_student(student_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    # Authorization check
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT and current_user["user_id"] != student_id:
        raise HTTPException(status_code=403, detail="Students can only access their own profile.")
    if role == UserRole.PARENT and student_id not in current_user.get("child_ids", []):
        raise HTTPException(status_code=403, detail="Parents can only access their linked child data.")

    student = MOCK_STUDENTS.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@app.get("/api/mock/students/{student_id}/attendance", summary="Get Student Attendance Records")
def get_student_attendance(student_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT and current_user["user_id"] != student_id:
        raise HTTPException(status_code=403, detail="Students can only view their own attendance.")
    if role == UserRole.PARENT and student_id not in current_user.get("child_ids", []):
        raise HTTPException(status_code=403, detail="Parents can only view their linked child's attendance.")

    student = MOCK_STUDENTS.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student attendance record not found.")
    return {
        "student_id": student["student_id"],
        "student_name": student["student_name"],
        "grade_section": student["grade_section"],
        "overall_percentage": student["overall_percentage"],
        "last_month_percentage": student["last_month_percentage"],
        "total_days": student["total_days"],
        "present_days": student["present_days"],
        "absent_days": student["absent_days"],
        "subject_wise": student["subject_wise"],
        "recent_logs": student["recent_logs"]
    }


@app.get("/api/mock/children/{parent_id}", summary="Get Linked Children for Parent")
def get_parent_children(parent_id: str, current_user: Dict[str, Any] = Depends(require_role([UserRole.PARENT, UserRole.PRINCIPAL]))):
    if UserRole(current_user["role"]) == UserRole.PARENT and current_user["user_id"] != parent_id:
        raise HTTPException(status_code=403, detail="Access denied to requested parent profile.")
    
    parent_user = None
    for u in MOCK_USERS.values():
        if u["user_id"] == parent_id and u["role"] == "PARENT":
            parent_user = u
            break
    if not parent_user:
        raise HTTPException(status_code=404, detail="Parent not found.")
    
    children_list = [MOCK_STUDENTS[cid] for cid in parent_user.get("child_ids", []) if cid in MOCK_STUDENTS]
    return children_list


@app.post("/api/mock/attendance/mark", response_model=AttendanceMarkResponse, summary="Mark Student Attendance (Teacher only)")
def mark_attendance(req: AttendanceMarkRequest, current_user: Dict[str, Any] = Depends(require_role([UserRole.TEACHER, UserRole.PRINCIPAL]))):
    student = MOCK_STUDENTS.get(req.student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {req.student_id} not found.")
    
    # Teacher boundary check
    if UserRole(current_user["role"]) == UserRole.TEACHER:
        if student["grade_section"] not in current_user.get("assigned_classes", []):
            raise HTTPException(status_code=403, detail=f"Teacher not authorized for grade {student['grade_section']}.")
    
    # Log entry
    new_log = {
        "date": req.date,
        "status": req.status.upper(),
        "subject": req.subject or "Overall",
        "remark": req.remarks or f"Marked by {current_user['name']}"
    }
    student["recent_logs"].insert(0, new_log)
    
    return AttendanceMarkResponse(
        success=True,
        record_id=f"REC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        student_id=req.student_id,
        student_name=student["student_name"],
        date=req.date,
        status=req.status.upper(),
        message=f"Successfully marked {student['student_name']} as {req.status.upper()} for {req.date}."
    )


@app.get("/api/mock/analytics/attendance", summary="Get School Analytics (Principal only)")
def get_analytics(current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL]))):
    return MOCK_ANALYTICS


@app.post("/api/mock/support/call-request", response_model=SupportCallResponse, summary="Create Teacher Call Request")
def create_support_call(req: SupportCallRequest, current_user: Dict[str, Any] = Depends(require_role([UserRole.PARENT, UserRole.PRINCIPAL]))):
    req_id = f"REQ-{len(MOCK_SUPPORT_REQUESTS) + 1001}"
    new_req = {
        "request_id": req_id,
        "parent_id": req.parent_id,
        "student_id": req.student_id,
        "teacher_id": req.teacher_id,
        "status": "SUBMITTED",
        "reason": req.reason,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
    MOCK_SUPPORT_REQUESTS.append(new_req)
    return SupportCallResponse(
        request_id=req_id,
        status="SUBMITTED",
        message=f"Call request {req_id} submitted to teacher. You will be contacted shortly.",
        timestamp=new_req["timestamp"]
    )


# ==========================================
# PARTH ASSISTANT AI CHAT API (PHASE 1 INTEGRATION)
# ==========================================

PERSONA_MAPPING = {
    UserRole.STUDENT: "Academic Assistant",
    UserRole.PARENT: "Parent Support Assistant",
    UserRole.TEACHER: "Teaching Assistant",
    UserRole.PRINCIPAL: "Management Assistant"
}

@app.post("/api/chat", response_model=ChatMessageResponse, summary="Parth Assistant AI Chat Endpoint")
def chat_with_parth(req: ChatMessageRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = UserRole(current_user["role"])
    persona = PERSONA_MAPPING.get(user_role, "Academic Assistant")
    msg = req.message.lower()
    
    # Phase 1 simple mock dispatcher (Agent workflow will be fully expanded in Phase 3 & 4)
    if "attendance" in msg or "kitni hai" in msg:
        if user_role == UserRole.STUDENT:
            student = MOCK_STUDENTS.get(current_user["user_id"], MOCK_STUDENTS["S101"])
            resp = f"Hi {current_user['name']}! You currently have {student['overall_percentage']}% overall attendance with {student['present_days']} days present."
        elif user_role == UserRole.PARENT:
            child_id = current_user.get("child_ids", ["S101"])[0]
            student = MOCK_STUDENTS.get(child_id, MOCK_STUDENTS["S101"])
            resp = f"Hello {current_user['name']}. {student['student_name']} currently has {student['overall_percentage']}% attendance ({student['present_days']}/{student['total_days']} days)."
        elif user_role == UserRole.TEACHER:
            resp = f"Hello {current_user['name']}. Class 10-A has an average attendance of 93.5% today. Would you like to mark attendance for any student?"
        else:
            resp = f"Respected {current_user['name']}, overall school attendance today is {MOCK_ANALYTICS['overall_attendance']}% across {MOCK_ANALYTICS['total_students']} students."
        intent = "VIEW_ATTENDANCE"
    elif "teacher" in msg or "call" in msg or "talk" in msg:
        resp = "I can submit a call request to your child's teacher. Would you like me to schedule that right away?"
        intent = "CONTACT_TEACHER"
    else:
        resp = f"Hello {current_user['name']}! I am Parth Assistant AI, your {persona}. How can I assist you today with school attendance, schedules, or support?"
        intent = "GREETING"

    return ChatMessageResponse(
        response=resp,
        role=user_role,
        persona=persona,
        intent=intent,
        entities={"user_id": current_user["user_id"]},
        action_taken=None,
        data={"user": current_user["name"]}
    )
