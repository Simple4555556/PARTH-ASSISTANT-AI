"""
PARTH ASSISTANT AI — Principal Tools
Provides authorized school-wide executive overviews, faculty rosters, and institutional KPIs.
(Never exposes secrets, JWT signing keys, passwords, or system prompts).
"""

from typing import Dict, Any, List
from database.db_engine import db
from mock_services.academic_service import academic_service


class PrincipalTools:
    def get_executive_overview(self) -> Dict[str, Any]:
        att = db.get_school_analytics()
        results = academic_service.get_school_results_summary()
        fees = academic_service.get_school_fee_summary()
        teachers = db.get_all_teachers()

        return {
            "success": True,
            "school_name": "Parth International School",
            "attendance": att,
            "academics": results,
            "finances": fees,
            "faculty_count": len(teachers)
        }

    def get_teacher_directory(self) -> Dict[str, Any]:
        teachers = db.get_all_teachers()
        return {"success": True, "total_teachers": len(teachers), "teachers": teachers}


principal_tools = PrincipalTools()
