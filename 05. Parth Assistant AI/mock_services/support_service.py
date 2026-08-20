"""
Mock ERP Service — Human Escalation & Support Requests Logic
"""

from typing import Dict, Any, Optional
from database.db_engine import db


class SupportService:
    def create_call_request(self, parent_id: str, student_id: str, teacher_id: str, reason: str) -> Dict[str, Any]:
        return db.create_support_request(parent_id, student_id, teacher_id, reason)

    def get_call_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        return db.get_support_request(request_id)


support_service = SupportService()
