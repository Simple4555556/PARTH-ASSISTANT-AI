"""
Attendance Agent — Specialized handler for attendance operations
"""

from typing import Dict, Any
from tools.attendance_tools import attendance_tools
from tools.student_tools import student_tools


class AttendanceAgent:
    def handle_query(self, user: Dict[str, Any], intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        role = user.get("role")
        user_id = user.get("user_id")

        if intent == "VIEW_OWN_ATTENDANCE":
            student_id = user_id if role == "STUDENT" else (entities.get("student_id") or "S101")
            res = attendance_tools.get_own_attendance(student_id)
            if res.get("success"):
                res["subject"] = entities.get("subject")
                res["entities"] = entities
            return res

        if intent == "VIEW_CHILD_ATTENDANCE":
            # Determine child student ID
            student_name = entities.get("student_name")
            if student_name:
                res = student_tools.resolve_student_by_name(student_name)
                if res.get("success") and res.get("student"):
                    child_id = res["student"]["student_id"]
                else:
                    child_ids = user.get("child_ids") or ["S101"]
                    child_id = child_ids[0] if child_ids else "S101"
            else:
                child_ids = user.get("child_ids") or ["S101"]
                child_id = child_ids[0] if child_ids else "S101"

            res = attendance_tools.get_child_attendance(child_id)
            if res.get("success"):
                res["subject"] = entities.get("subject")
                res["entities"] = entities
            return res

        if intent == "VIEW_RECENT_ATTENDANCE":
            student_name = entities.get("student_name")
            if student_name:
                res = student_tools.resolve_student_by_name(student_name)
                child_id = res["student"]["student_id"] if (res.get("success") and res.get("student")) else "S101"
            else:
                child_ids = user.get("child_ids") or []
                child_id = child_ids[0] if child_ids else (user.get("user_id") or "S101")

            return attendance_tools.get_recent_attendance(child_id, limit=5)

        if intent == "MARK_ATTENDANCE":
            student_name = entities.get("student_name", "Rahul")
            res = student_tools.resolve_student_by_name(student_name)
            if not res.get("success"):
                return {"success": False, "error": f"Student '{student_name}' not found to mark attendance."}
            
            target_student = res["student"]
            status = entities.get("attendance_status", "ABSENT")
            subject = entities.get("subject", "Overall")
            date = entities.get("date", "2026-08-20")
            if date == "today":
                date = "2026-08-20"

            return attendance_tools.mark_student_attendance(
                student_id=target_student["student_id"],
                date=date,
                status=status,
                subject=subject,
                remarks=f"Marked by {user['name']}"
            )

        return {"success": False, "error": "Unhandled attendance intent."}


attendance_agent = AttendanceAgent()
