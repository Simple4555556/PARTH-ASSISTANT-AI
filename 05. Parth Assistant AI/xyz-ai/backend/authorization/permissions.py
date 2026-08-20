"""
PARTH ASSISTANT AI — Centralized RBAC Permissions & Matrix (Phase 4 Conversational-First)
"""

from typing import Dict, List

ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "STUDENT": [
        "VIEW_OWN_ATTENDANCE",
        "VIEW_RECENT_ATTENDANCE",
        "VIEW_TIMETABLE",
        "VIEW_TEACHERS",
        "GREETING",
        "HELP",
        "OPEN_DASHBOARD"
    ],
    "PARENT": [
        "VIEW_CHILD_ATTENDANCE",
        "VIEW_RECENT_ATTENDANCE",
        "CONTACT_TEACHER",
        "VIEW_TIMETABLE",
        "VIEW_TEACHERS",
        "GREETING",
        "HELP",
        "OPEN_DASHBOARD"
    ],
    "TEACHER": [
        "VIEW_CLASS_ATTENDANCE",
        "VIEW_STUDENT_ATTENDANCE",
        "VIEW_RECENT_ATTENDANCE",
        "MARK_ATTENDANCE",
        "VIEW_CLASS_ANALYTICS",
        "VIEW_TIMETABLE",
        "GREETING",
        "HELP",
        "OPEN_DASHBOARD"
    ],
    "PRINCIPAL": [
        "VIEW_SCHOOL_ANALYTICS",
        "VIEW_CLASS_ANALYTICS",
        "VIEW_STUDENT_ATTENDANCE",
        "VIEW_RECENT_ATTENDANCE",
        "VIEW_TEACHERS",
        "VIEW_TIMETABLE",
        "DATABASE_ACCESS",
        "VIEW_DATABASE",
        "GREETING",
        "HELP",
        "OPEN_DASHBOARD"
    ]
}


def is_action_permitted(role: str, action: str) -> bool:
    """Checks if action is allowed by role."""
    allowed = ROLE_PERMISSIONS.get(role.upper(), [])
    return action in allowed or action in ["GREETING", "HELP", "UNKNOWN", "CONFIRMATION", "OPEN_DASHBOARD"]
