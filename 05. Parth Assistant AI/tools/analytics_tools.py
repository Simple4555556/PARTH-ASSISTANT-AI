"""
PARTH ASSISTANT AI — Analytics Tools
Provides tools for school-wide KPIs, class-wise attendance, and performance analytics.
"""

from typing import Dict, Any, Optional
from mock_services.analytics_service import analytics_service
from database.db_engine import db


class AnalyticsTools:
    def get_overall_school_analytics(self) -> Dict[str, Any]:
        data = analytics_service.get_overall_analytics()
        return {"success": True, "data": data}

    def get_class_analytics(self, class_name: str) -> Dict[str, Any]:
        try:
            data = analytics_service.get_class_analytics(class_name)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_daily_absences(self, date: str = "2026-08-19", class_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            data = db.get_daily_absences(date, class_id)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}


analytics_tools = AnalyticsTools()
