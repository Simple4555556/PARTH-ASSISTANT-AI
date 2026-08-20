"""
Analytics Agent — Specialized handler for management & class analytics
"""

from typing import Dict, Any
from tools.analytics_tools import analytics_tools


class AnalyticsAgent:
    def handle_query(self, user: Dict[str, Any], intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        if intent == "VIEW_CLASS_ANALYTICS":
            class_name = entities.get("class_name", "10-A")
            return analytics_tools.get_class_analytics(class_name)

        # Default to overall school analytics
        return analytics_tools.get_overall_school_analytics()


analytics_agent = AnalyticsAgent()
