"""
PARTH ASSISTANT AI — Support Tools
Provides tools for creating and tracking teacher call requests.
"""

from typing import Dict, Any
from mock_services.support_service import support_service


class SupportTools:
    def create_call_request(self, parent_id: str, student_id: str, teacher_id: str, reason: str) -> Dict[str, Any]:
        rec = support_service.create_call_request(parent_id, student_id, teacher_id, reason)
        return {"success": True, "data": rec}

    def get_support_request(self, request_id: str) -> Dict[str, Any]:
        rec = support_service.get_call_request(request_id)
        if not rec:
            return {"success": False, "error": f"Request {request_id} not found."}
        return {"success": True, "data": rec}


support_tools = SupportTools()
