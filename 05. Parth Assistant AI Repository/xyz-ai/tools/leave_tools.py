"""
PARTH ASSISTANT AI — Leave Tools
Provides tools for student leave tracking.
"""

from typing import Dict, Any
from mock_services.academic_service import academic_service


class LeaveTools:
    def get_student_leaves(self, student_id: str) -> Dict[str, Any]:
        leaves = academic_service.get_student_leaves(student_id)
        return {"success": True, "student_id": student_id, "leave_records": leaves}


leave_tools = LeaveTools()
