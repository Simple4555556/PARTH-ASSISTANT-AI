"""
PARTH ASSISTANT AI — Attendance Tools
Provides validated tool endpoints for attendance queries and marking.
"""

from typing import Dict, Any, Optional
from mock_services.attendance_service import attendance_service


class AttendanceTools:
    def get_own_attendance(self, student_id: str) -> Dict[str, Any]:
        att = attendance_service.get_student_attendance(student_id)
        if not att:
            return {"success": False, "error": f"Student attendance not found for ID {student_id}"}
        return {"success": True, "data": att}

    def get_child_attendance(self, child_id: str) -> Dict[str, Any]:
        att = attendance_service.get_student_attendance(child_id)
        if not att:
            return {"success": False, "error": f"Child attendance not found for ID {child_id}"}
        return {"success": True, "data": att}

    def get_recent_attendance(self, student_id: str, limit: int = 5) -> Dict[str, Any]:
        logs = attendance_service.get_recent_attendance(student_id, limit)
        return {"success": True, "student_id": student_id, "logs": logs}

    def mark_student_attendance(self, student_id: str, date: str, status: str, subject: str = "Overall", remarks: Optional[str] = None) -> Dict[str, Any]:
        try:
            res = attendance_service.mark_attendance(student_id, date, status, subject, remarks)
            return {"success": True, "data": res}
        except Exception as e:
            return {"success": False, "error": str(e)}


attendance_tools = AttendanceTools()
