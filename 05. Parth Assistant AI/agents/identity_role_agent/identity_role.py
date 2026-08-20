"""
Identity & Role Agent — Extracts role & user_id strictly from session JWT data
"""

from typing import Dict, Any


class IdentityRoleAgent:
    def get_authenticated_identity(self, session_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Derives authenticated user identity and role.
        NEVER trusts natural-language claims inside the prompt.
        """
        user_id = session_user.get("user_id", "ANONYMOUS")
        role = session_user.get("role", "STUDENT")
        name = session_user.get("name", "User")
        child_ids = session_user.get("child_ids", [])
        assigned_classes = session_user.get("assigned_classes", [])

        return {
            "user_id": user_id,
            "role": role,
            "name": name,
            "child_ids": child_ids,
            "assigned_classes": assigned_classes
        }


identity_agent = IdentityRoleAgent()
