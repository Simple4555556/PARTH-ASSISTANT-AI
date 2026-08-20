"""
PARTH ASSISTANT AI — Mock School ERP APIRouter
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status

from .models import (
    UserRole, AttendanceMarkRequest, AttendanceMarkResponse,
    SupportCallRequest, SupportCallResponse
)
from .auth import get_current_user, require_role
from mock_services.student_service import student_service
from mock_services.attendance_service import attendance_service
from mock_services.analytics_service import analytics_service
from mock_services.support_service import support_service

router = APIRouter(prefix="/api/mock", tags=["Mock School ERP"])


@router.get("/students/{student_id}")
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


@router.get("/students/{student_id}/attendance")
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


@router.get("/students/{student_id}/attendance/recent")
def get_student_recent_attendance(student_id: str, limit: int = 5, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = UserRole(current_user["role"])
    if role == UserRole.STUDENT and current_user["user_id"] != student_id:
        raise HTTPException(status_code=403, detail="Students can only view their own attendance logs.")
    if role == UserRole.PARENT and student_id not in current_user.get("child_ids", []):
        raise HTTPException(status_code=403, detail="Parents can only view their linked child's attendance logs.")

    return attendance_service.get_recent_attendance(student_id, limit)


@router.get("/children/{parent_id}")
def get_parent_children(parent_id: str, current_user: Dict[str, Any] = Depends(require_role([UserRole.PARENT, UserRole.PRINCIPAL]))):
    if UserRole(current_user["role"]) == UserRole.PARENT and current_user["user_id"] != parent_id:
        raise HTTPException(status_code=403, detail="Access denied to requested parent profile.")

    children = student_service.get_parent_children(parent_id)
    if not children:
        raise HTTPException(status_code=404, detail="No linked children found for this parent.")
    return children


@router.post("/attendance/mark", response_model=AttendanceMarkResponse)
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


@router.get("/analytics/attendance")
def get_analytics(current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL]))):
    return analytics_service.get_overall_analytics()


@router.get("/analytics/class/{class_name}")
def get_class_analytics(class_name: str, current_user: Dict[str, Any] = Depends(require_role([UserRole.PRINCIPAL, UserRole.TEACHER]))):
    try:
        return analytics_service.get_class_analytics(class_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/support/call-request", response_model=SupportCallResponse)
def create_support_call(req: SupportCallRequest, current_user: Dict[str, Any] = Depends(require_role([UserRole.PARENT, UserRole.PRINCIPAL]))):
    rec = support_service.create_call_request(req.parent_id, req.student_id, req.teacher_id, req.reason)
    return SupportCallResponse(
        request_id=rec["request_id"],
        status="SUBMITTED",
        message=f"Call request {rec['request_id']} successfully submitted to teacher.",
        timestamp=rec["timestamp"]
    )


@router.get("/support/request/{request_id}")
def get_support_request(request_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    rec = support_service.get_call_request(request_id)
    if not rec:
        raise HTTPException(status_code=404, detail=f"Support request {request_id} not found.")
    return rec


@router.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    teacher = student_service.get_teacher_by_id(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail=f"Teacher {teacher_id} not found.")
    return teacher
