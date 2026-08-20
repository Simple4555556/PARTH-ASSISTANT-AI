"""
PARTH ASSISTANT AI — Student Tools
Provides tools for student profile lookups and parent-child mapping.
"""

from typing import Dict, Any, Optional
from mock_services.student_service import student_service
from database.db_engine import db


class StudentTools:
    def get_student_profile(self, student_id: str) -> Dict[str, Any]:
        student = student_service.get_student_by_id(student_id)
        if not student:
            return {"success": False, "error": f"Student {student_id} not found."}
        return {"success": True, "data": student}

    def resolve_student_by_name(self, name_query: str) -> Dict[str, Any]:
        name_lower = name_query.lower()
        matches = []
        for s in db.students.values():
            if name_lower in s["student_name"].lower():
                matches.append(s)
        if not matches:
            return {"success": False, "count": 0, "error": f"No student matching '{name_query}' found."}
        if len(matches) > 1:
            return {"success": True, "count": len(matches), "matches": matches, "disambiguation_needed": True}
        return {"success": True, "count": 1, "student": matches[0], "disambiguation_needed": False}

    def get_linked_children(self, parent_id: str) -> Dict[str, Any]:
        children = student_service.get_parent_children(parent_id)
        return {"success": True, "children": children}


student_tools = StudentTools()
