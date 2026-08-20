"""
Mock ERP Service — Student & Parent Operations
"""

from typing import Dict, Any, List, Optional
from database.db_engine import db


class StudentService:
    def get_student_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        return db.get_student(student_id)

    def get_parent_children(self, parent_id: str) -> List[Dict[str, Any]]:
        return db.get_children_for_parent(parent_id)

    def get_teacher_by_id(self, teacher_id: str) -> Optional[Dict[str, Any]]:
        return db.get_teacher(teacher_id)


student_service = StudentService()
