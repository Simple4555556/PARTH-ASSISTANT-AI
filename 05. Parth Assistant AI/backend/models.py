"""
PARTH ASSISTANT AI — Data Models & Schemas
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    PARENT = "PARENT"
    TEACHER = "TEACHER"
    PRINCIPAL = "PRINCIPAL"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    role: UserRole
    name: str
    child_ids: Optional[List[str]] = None
    assigned_classes: Optional[List[str]] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class StudentRegisterRequest(BaseModel):
    username: str
    name: str
    email: str
    password: str
    confirm_password: str
    student_id: Optional[str] = None
    grade_section: Optional[str] = "10-A"


class ParentRegisterRequest(BaseModel):
    username: str
    name: str
    email: str
    password: str
    confirm_password: str
    linked_student_id: str


class TeacherRegisterRequest(BaseModel):
    username: str
    name: str
    email: str
    password: str
    confirm_password: str
    subject: str = "General"
    verification_code: str  # Teacher staff verification code (e.g. TEACHER2026)


class RegisterResponse(BaseModel):
    success: bool
    message: str
    user_id: str
    username: str
    role: UserRole



class UserProfile(BaseModel):
    user_id: str
    username: str
    role: UserRole
    name: str
    email: str
    avatar_url: Optional[str] = None
    child_ids: Optional[List[str]] = None
    assigned_classes: Optional[List[str]] = None


class StudentAttendance(BaseModel):
    student_id: str
    student_name: str
    grade_section: str
    overall_percentage: float
    total_days: int
    present_days: int
    absent_days: int
    leave_days: int
    subject_wise: Dict[str, float]
    recent_logs: List[Dict[str, Any]]


class AttendanceMarkRequest(BaseModel):
    student_id: str
    date: str
    status: str  # PRESENT, ABSENT, LEAVE
    subject: Optional[str] = "Overall"
    remarks: Optional[str] = None


class AttendanceMarkResponse(BaseModel):
    success: bool
    record_id: str
    student_id: str
    student_name: str
    date: str
    status: str
    message: str


class SchoolAnalytics(BaseModel):
    overall_attendance: float
    total_students: int
    present_today: int
    absent_today: int
    class_wise_attendance: Dict[str, float]
    monthly_trends: List[Dict[str, Any]]


class SupportCallRequest(BaseModel):
    parent_id: str
    student_id: str
    teacher_id: str
    reason: str
    preferred_time: Optional[str] = "As soon as possible"


class SupportCallResponse(BaseModel):
    request_id: str
    status: str  # SUBMITTED, PENDING, CONFIRMED
    message: str
    timestamp: str


class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    language: Optional[str] = "en"


class ChatMessageResponse(BaseModel):
    message: str
    response: Optional[str] = None
    ui_action: str = "NONE"
    component: Optional[str] = None
    data: Optional[Dict[str, Any]] = {}
    role: UserRole
    persona: str
    intent: Optional[str] = "GREETING"
    entities: Optional[Dict[str, Any]] = {}
    tool_used: Optional[str] = None
    action_taken: Optional[str] = None
    success: bool = True

