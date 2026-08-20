"""
Mock ERP Service — School Analytics & Class Statistics Logic
"""

from typing import Dict, Any
from database.db_engine import db


class AnalyticsService:
    def get_overall_analytics(self) -> Dict[str, Any]:
        return db.get_school_analytics()

    def get_class_analytics(self, class_name: str) -> Dict[str, Any]:
        return db.get_class_analytics(class_name)


analytics_service = AnalyticsService()
