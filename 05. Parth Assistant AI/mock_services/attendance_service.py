"""
Mock ERP Service — Attendance Query & Modification Logic
"""

from typing import Dict, Any, List, Optional
from database.db_engine import db


class AttendanceService:
    def get_student_attendance(self, student_id: str) -> Optional[Dict[str, Any]]:
        return db.get_attendance(student_id)

    def get_recent_attendance(self, student_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        return db.get_recent_attendance(student_id, limit)

    def mark_attendance(self, student_id: str, date: str, status: str, subject: str = "Overall", remarks: Optional[str] = None) -> Dict[str, Any]:
        return db.mark_attendance(student_id, date, status, subject, remarks)


attendance_service = AttendanceService()
