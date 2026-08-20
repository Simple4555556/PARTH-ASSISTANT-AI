"""
Escalation Agent — Manages teacher call request confirmation workflow
"""

from typing import Dict, Any
from tools.support_tools import support_tools
from tools.student_tools import student_tools


class EscalationAgent:
    def handle_request(self, user: Dict[str, Any], message: str, pending_confirmation: bool, entities: Dict[str, Any]) -> Dict[str, Any]:
        msg_lower = message.lower().strip()

        # Step 1: Initial request -> Ask for confirmation
        if not pending_confirmation:
            if not any(k in msg_lower for k in ["yes", "confirm", "sure", "proceed"]):
                student_name = entities.get("student_name", "Rahul")
                return {
                    "step": "ASK_CONFIRMATION",
                    "requires_user_confirmation": True,
                    "message": f"Of course. Would you like me to submit a call request to {student_name}'s class teacher?"
                }

        # Step 2: User confirmed -> Execute support tool API
        parent_id = user.get("user_id", "P201")
        student_id = "S101"
        teacher_id = "T301"

        res = support_tools.create_call_request(
            parent_id=parent_id,
            student_id=student_id,
            teacher_id=teacher_id,
            reason=f"Teacher call request submitted by {user.get('name')}"
        )

        if res.get("success"):
            req_data = res["data"]
            return {
                "step": "SUBMITTED",
                "requires_user_confirmation": False,
                "request_id": req_data["request_id"],
                "message": f"Your call request has been submitted successfully. Your request ID is {req_data['request_id']}."
            }

        return {
            "step": "FAILED",
            "requires_user_confirmation": False,
            "message": "The call request could not be submitted right now. Please try again shortly."
        }


escalation_agent = EscalationAgent()
