"""
PARTH ASSISTANT AI — Analytics Tools
Provides tools for school-wide KPIs and class-wise performance analytics.
"""

from typing import Dict, Any
from mock_services.analytics_service import analytics_service


class AnalyticsTools:
    def get_overall_school_analytics(Com) -> Dict[str, Any]:
        data = analytics_service.get_overall_analytics()
        return {"success": True, "data": data}

    def get_class_analytics(self, class_name: str) -> Dict[str, Any]:
        try:
            data = analytics_service.get_class_analytics(class_name)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}


analytics_tools = AnalyticsTools()
