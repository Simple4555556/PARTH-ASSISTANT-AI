"""
PARTH ASSISTANT AI — Teacher Analytics Tools
Provides tools for teacher workload, classes conducted, and attendance marking compliance.
"""

from typing import Dict, Any, List
from database.db_engine import db


class TeacherAnalyticsTools:
    def get_teacher_analytics(self, teacher_id: str) -> Dict[str, Any]:
        try:
            data = db.get_teacher_analytics(teacher_id)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_teachers_summary(self) -> Dict[str, Any]:
        teachers = db.get_all_teachers()
        return {"success": True, "total_teachers": len(teachers), "teachers": teachers}


teacher_analytics_tools = TeacherAnalyticsTools()
