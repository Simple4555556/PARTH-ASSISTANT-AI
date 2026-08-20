"""
PARTH ASSISTANT AI — Marks & Exam Analytics Tools
Provides secure tool endpoints for student marks, subject-wise pass/fail, and exam results.
"""

from typing import Dict, Any, Optional, List
from mock_services.academic_service import academic_service


class MarksTools:
    def get_student_marks(self, student_id: str, exam_name: Optional[str] = None) -> Dict[str, Any]:
        marks = academic_service.get_student_marks(student_id, exam_name)
        if not marks:
            return {"success": False, "error": f"No marks found for student {student_id}"}
        return {"success": True, "student_id": student_id, "data": marks}

    def get_subject_results(self, subject_name: str, class_name: Optional[str] = None) -> Dict[str, Any]:
        data = academic_service.get_subject_results(subject_name, class_name)
        return {"success": True, "data": data}

    def get_school_results(self) -> Dict[str, Any]:
        data = academic_service.get_school_results_summary()
        return {"success": True, "data": data}


marks_tools = MarksTools()
