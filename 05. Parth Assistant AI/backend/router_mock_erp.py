"""
PARTH ASSISTANT AI — School ERP APIRouter (REST Endpoints & Role Authorization)
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from .models import (
    UserRole, AttendanceMarkRequest, AttendanceMarkResponse,
    SupportCallRequest, SupportCallResponse
)
from .auth import get_current_user, require_role
from mock_services.student_service import student_service
from mock_services.attendance_service import attendance_service
from mock_services.analytics_service import analytics_service
from mock_services.support_service import support_service
from mock_services.academic_service import academic_service
from database.db_engine import db

router = APIRouter(tags=["School ERP"])


# ── Student Endpoints ──────────────────────────────────────────────────
@router.get("/api/students/me", summary="Get Authenticated Student Profile")
def get_my_student_profile(current_user: Dict[str, Any] = Depends(require_role([UserRole.STUDENT]))):
    student = student_service.get_student_by_id(current_user["user_id"])
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    return student


@router.get("/api/students/{student_id}", summary="Get Student Details by ID")
@router.get("/api/mock/students/{student_id}", include_in_schema=False)
def get_student(student_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT and current_user["user_id"] != student_id:
        raise HTTPException(status_code=403, detail="Students can only access their own profile.")
    if role == UserRole.PARENT and student_id not in current_user.get("child_ids", []):
        raise HTTPException(status_code=403, detail="Parents can only access their linked child data.")

    student = student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found.")
    return student


@router.get("/api/students/{student_id}/attendance", summary="Get Student Attendance Summary")
@router.get("/api/mock/students/{student_id}/attendance", include_in_schema=False)
def get_student_attendance(student_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT and current_user["user_id"] != student_id:
        raise HTTPException(status_code=403, detail="Students can only view their own attendance.")
    if role == UserRole.PARENT and student_id not in current_user.get("child_ids", []):
        raise HTTPException(status_code=403, detail="Parents can only view their linked child's attendance.")

    att = attendance_service.get_student_attendance(student_id)
    if not att:
        raise HTTPException(status_code=404, detail=f"Attendance record for student {student_id} not found.")
    return att


@router.get("/api/students/{student_id}/attendance/recent", summary="Get Recent Attendance Logs")
@router.get("/api/mock/students/{student_id}/attendance/recent", include_in_schema=False)
def get_student_recent_attendance(student_id: str, limit: int = 5, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT and current_user["user_id"] != student_id:
        raise HTTPException(status_code=403, detail="Students can only view their own attendance logs.")
    if role == UserRole.PARENT and student_id not in current_user.get("child_ids", []):
        raise HTTPException(status_code=403, detail="Parents can only view their linked child's attendance logs.")

    return attendance_service.get_recent_attendance(student_id, limit)


@router.get("/api/students/{student_id}/marks", summary="Get Student Marks & Grades")
def get_student_marks(student_id: str, exam_name: Optional[str] = None, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT and current_user["user_id"] != student_id:
        raise HTTPException(status_code=403, detail="Students can only view their own marks.")
    if role == UserRole.PARENT and student_id not in current_user.get("child_ids", []):
        raise HTTPException(status_code=403, detail="Parents can only view their linked child's marks.")

    marks = academic_service.get_student_marks(student_id, exam_name)
    return {"student_id": student_id, "marks": marks}


# ── Parent Endpoints ───────────────────────────────────────────────────
@router.get("/api/children/{parent_id}", summary="Get Linked Children for Parent")
@router.get("/api/mock/children/{parent_id}", include_in_schema=False)
def get_parent_children(parent_id: str, current_user: Dict[str, Any] = Depends(require_role([UserRole.PARENT, UserRole.PRINCIPAL]))):
    if UserRole(current_user["role"]) == UserRole.PARENT and current_user["user_id"] != parent_id:
        raise HTTPException(status_code=403, detail="Access denied to requested parent profile.")

    children = student_service.get_parent_children(parent_id)
    if not children:
        raise HTTPException(status_code=404, detail="No linked children found for this parent.")
    return children


# ── Teacher Endpoints ──────────────────────────────────────────────────
@router.get("/api/teachers", summary="Get All Faculty Members (Principal only)")
def get_all_teachers(current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL]))):
    return db.get_all_teachers()


@router.get("/api/teachers/{teacher_id}", summary="Get Teacher Details")
@router.get("/api/mock/teachers/{teacher_id}", include_in_schema=False)
def get_teacher(teacher_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    teacher = student_service.get_teacher_by_id(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail=f"Teacher {teacher_id} not found.")
    return teacher


@router.get("/api/teachers/{teacher_id}/analytics", summary="Get Teacher Performance & Activity Analytics")
def get_teacher_analytics(teacher_id: str, current_user: Dict[str, Any] = Depends(require_role([UserRole.TEACHER, UserRole.PRINCIPAL]))):
    if UserRole(current_user["role"]) == UserRole.TEACHER and current_user["user_id"] != teacher_id:
        raise HTTPException(status_code=403, detail="Teachers can only view their own analytics.")
    try:
        return db.get_teacher_analytics(teacher_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Attendance Marking ─────────────────────────────────────────────────
@router.post("/api/attendance/mark", response_model=AttendanceMarkResponse, summary="Mark Student Attendance")
@router.post("/api/mock/attendance/mark", response_model=AttendanceMarkResponse, include_in_schema=False)
def mark_attendance(req: AttendanceMarkRequest, current_user: Dict[str, Any] = Depends(require_role([UserRole.TEACHER, UserRole.PRINCIPAL]))):
    student = student_service.get_student_by_id(req.student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {req.student_id} not found.")

    if UserRole(current_user["role"]) == UserRole.TEACHER:
        if student["grade_section"] not in current_user.get("assigned_classes", []):
            raise HTTPException(status_code=403, detail=f"Teacher not authorized to mark attendance for grade {student['grade_section']}.")

    res = attendance_service.mark_attendance(req.student_id, req.date, req.status, req.subject or "Overall", req.remarks)
    return AttendanceMarkResponse(
        success=True,
        record_id=f"REC-{req.student_id}-{req.date}",
        student_id=req.student_id,
        student_name=res["student_name"],
        date=req.date,
        status=res["status"],
        message=f"Attendance updated for {res['student_name']}. New overall percentage: {res['new_overall_percentage']}%."
    )


# ── Analytics & Academic Performance ──────────────────────────────────
@router.get("/api/analytics/attendance", summary="Get School-Wide Attendance KPIs")
@router.get("/api/mock/analytics/attendance", include_in_schema=False)
def get_analytics(current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL]))):
    return analytics_service.get_overall_analytics()


@router.get("/api/analytics/class/{class_name}", summary="Get Class-Wise Attendance")
@router.get("/api/mock/analytics/class/{class_name}", include_in_schema=False)
def get_class_analytics(class_name: str, current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL, UserRole.TEACHER]))):
    try:
        return analytics_service.get_class_analytics(class_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/api/classes/{class_id}/attendance", summary="Get Class Attendance Analytics")
def get_class_attendance(class_id: str, current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL, UserRole.TEACHER]))):
    try:
        return analytics_service.get_class_analytics(class_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/api/subjects/{subject_id}/results", summary="Get Subject Performance & Pass/Fail Ratio")
def get_subject_results(subject_id: str, class_name: Optional[str] = None, current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL, UserRole.TEACHER]))):
    return academic_service.get_subject_results(subject_id, class_name)


@router.get("/api/analytics/results", summary="Get School-Wide Academic Results")
def get_school_results(current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL]))):
    return academic_service.get_school_results_summary()


# ── Timetable ──────────────────────────────────────────────────────────
@router.get("/api/timetable", summary="Get Timetable for Class or Teacher")
def get_timetable(class_id: Optional[str] = None, teacher_id: Optional[str] = None, day: Optional[str] = None, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    
    if role == UserRole.STUDENT:
        student = student_service.get_student_by_id(current_user["user_id"])
        c_id = student["class_id"] if student else "C-10A"
        return academic_service.get_class_timetable(c_id, day)
    elif role == UserRole.PARENT:
        child_id = current_user.get("child_ids", ["S101"])[0]
        student = student_service.get_student_by_id(child_id)
        c_id = student["class_id"] if student else "C-10A"
        return academic_service.get_class_timetable(c_id, day)
    elif role == UserRole.TEACHER:
        t_id = teacher_id or current_user["user_id"]
        return academic_service.get_teacher_timetable(t_id, day)
    else:
        # Principal
        if class_id:
            return academic_service.get_class_timetable(class_id, day)
        elif teacher_id:
            return academic_service.get_teacher_timetable(teacher_id, day)
        return academic_service.get_class_timetable("C-10A", day)


# ── Assignments & Homework ─────────────────────────────────────────────
@router.get("/api/assignments", summary="Get Assignments")
def get_assignments(class_id: Optional[str] = None, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT:
        student = student_service.get_student_by_id(current_user["user_id"])
        c_id = student["class_id"] if student else "C-10A"
    elif role == UserRole.PARENT:
        child_id = current_user.get("child_ids", ["S101"])[0]
        student = student_service.get_student_by_id(child_id)
        c_id = student["class_id"] if student else "C-10A"
    else:
        c_id = class_id or "C-10A"
    return academic_service.get_class_assignments(c_id)


# ── Leave Requests ─────────────────────────────────────────────────────
@router.get("/api/leave", summary="Get Leave Requests")
def get_leave_requests(student_id: Optional[str] = None, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT:
        s_id = current_user["user_id"]
    elif role == UserRole.PARENT:
        s_id = student_id or current_user.get("child_ids", ["S101"])[0]
        if s_id not in current_user.get("child_ids", []):
            raise HTTPException(status_code=403, detail="Parents can only view leaves for their linked children.")
    else:
        s_id = student_id or "S101"
    return academic_service.get_student_leaves(s_id)


# ── Fees ───────────────────────────────────────────────────────────────
@router.get("/api/fees", summary="Get Student Fee Details or School Summary")
def get_fees(student_id: Optional[str] = None, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    
    if role == UserRole.STUDENT:
        return academic_service.get_student_fees(current_user["user_id"])
    elif role == UserRole.PARENT:
        s_id = student_id or current_user.get("child_ids", ["S101"])[0]
        if s_id not in current_user.get("child_ids", []):
            raise HTTPException(status_code=403, detail="Parents can only view fees for their linked children.")
        return academic_service.get_student_fees(s_id)
    elif role == UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Teachers are not authorized to view student financial and fee records.")
    elif role == UserRole.PRINCIPAL:
        if student_id:
            return academic_service.get_student_fees(student_id)
        return academic_service.get_school_fee_summary()


# ── Support Requests ───────────────────────────────────────────────────
class SupportCreatePayload(BaseModel):
    parent_id: str
    student_id: str
    teacher_id: str
    reason: str


@router.post("/api/support/request", response_model=SupportCallResponse, summary="Create Support Request")
@router.post("/api/mock/support/call-request", response_model=SupportCallResponse, include_in_schema=False)
def create_support_call(req: SupportCallRequest, current_user: Dict[str, Any] = Depends(require_role([UserRole.PARENT, UserRole.PRINCIPAL]))):
    rec = support_service.create_call_request(req.parent_id, req.student_id, req.teacher_id, req.reason)
    return SupportCallResponse(
        request_id=rec["request_id"],
        status="SUBMITTED",
        message=f"Call request {rec['request_id']} successfully submitted to teacher.",
        timestamp=rec["timestamp"]
    )


@router.get("/api/support/request/{request_id}", summary="Get Support Request Details")
@router.get("/api/mock/support/request/{request_id}", include_in_schema=False)
def get_support_request(request_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    rec = support_service.get_call_request(request_id)
    if not rec:
        raise HTTPException(status_code=404, detail=f"Support request {request_id} not found.")
    return rec
