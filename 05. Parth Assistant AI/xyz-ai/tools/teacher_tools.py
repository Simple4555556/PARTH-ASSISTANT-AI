"""
PARTH ASSISTANT AI — Teacher Tools
Provides tools for teacher assignment lookups.
"""

from typing import Dict, Any
from mock_services.student_service import student_service


class TeacherTools:
    def get_teacher_profile(self, teacher_id: str) -> Dict[str, Any]:
        teacher = student_service.get_teacher_by_id(teacher_id)
        if not teacher:
            return {"success": False, "error": f"Teacher {teacher_id} not found."}
        return {"success": True, "data": teacher}


teacher_tools = TeacherTools()
