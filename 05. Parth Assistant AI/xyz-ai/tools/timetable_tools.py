"""
PARTH ASSISTANT AI — Timetable Tools
Provides schedule lookup for classes and teachers.
"""

from typing import Dict, Any, Optional
from mock_services.academic_service import academic_service


class TimetableTools:
    def get_class_timetable(self, class_id: str, day: Optional[str] = None) -> Dict[str, Any]:
        slots = academic_service.get_class_timetable(class_id, day)
        return {"success": True, "class_id": class_id, "day": day or "ALL", "timetable": slots}

    def get_teacher_timetable(self, teacher_id: str, day: Optional[str] = None) -> Dict[str, Any]:
        slots = academic_service.get_teacher_timetable(teacher_id, day)
        return {"success": True, "teacher_id": teacher_id, "day": day or "ALL", "timetable": slots}


timetable_tools = TimetableTools()
