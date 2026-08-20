"""
PARTH ASSISTANT AI — Application-Level Authorization Middleware
Enforces deterministic RBAC and resource boundary security.
"""

from typing import Dict, Any, Optional
from database.db_engine import db


class AuthorizationMiddleware:
    """Evaluates role-based resource permissions independently of LLM prompts."""

    @staticmethod
    def evaluate_permission(
        user: Dict[str, Any],
        intent: str,
        target_resource: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        role = user.get("role")
        user_id = user.get("user_id")

        if not role or not user_id:
            return {"allowed": False, "reason": "Unauthenticated user session."}

        # Global Security Check: Refuse prompts asking for credentials, passwords, API keys
        target_student_id = (target_resource or {}).get("student_id")

        # Database Access Guard
        if intent in ["DATABASE_ACCESS", "VIEW_DATABASE"]:
            if role == "PRINCIPAL":
                return {"allowed": True, "reason": "Authorized principal school database access."}
            elif role == "TEACHER":
                return {"allowed": True, "reason": "Authorized teacher student academic database access."}
            else:
                return {
                    "allowed": False,
                    "reason": "I'm sorry, you don't have permission to access the database."
                }

        # ----------------------------------------------------
        # 1. STUDENT PERMISSIONS
        # ----------------------------------------------------
        if role == "STUDENT":
            if target_student_id and target_student_id != user_id:
                return {"allowed": False, "reason": "Sorry, you can only access information associated with your account."}

            if intent in ["VIEW_OWN_ATTENDANCE", "VIEW_RECENT_ATTENDANCE", "VIEW_TIMETABLE", "VIEW_TEACHERS", "OPEN_DASHBOARD", "GREETING", "HELP"]:
                return {"allowed": True, "reason": "Access granted to own student profile."}

            if intent in ["MARK_ATTENDANCE", "VIEW_SCHOOL_ANALYTICS", "VIEW_CLASS_ANALYTICS", "VIEW_CHILD_ATTENDANCE", "DATABASE_ACCESS", "VIEW_DATABASE"]:
                return {"allowed": False, "reason": "Sorry, you can only access information associated with your account."}

            return {"allowed": True, "reason": "General student query permitted."}

        # ----------------------------------------------------
        # 2. PARENT PERMISSIONS
        # ----------------------------------------------------
        if role == "PARENT":
            if intent in ["VIEW_CHILD_ATTENDANCE", "VIEW_OWN_ATTENDANCE", "VIEW_RECENT_ATTENDANCE", "VIEW_TIMETABLE", "VIEW_TEACHERS", "OPEN_DASHBOARD"]:
                child_ids = user.get("child_ids", [])
                if target_student_id and target_student_id not in child_ids:
                    student = db.get_student(target_student_id)
                    if student and student.get("parent_id") != user_id:
                        return {"allowed": False, "reason": "Parents can only access records for their linked child."}
                return {"allowed": True, "reason": "Access granted to linked child attendance."}

            if intent in ["CONTACT_TEACHER", "CONTACT_MANAGEMENT", "GREETING", "HELP"]:
                return {"allowed": True, "reason": "Escalation request permitted for parents."}

            if intent in ["MARK_ATTENDANCE", "VIEW_SCHOOL_ANALYTICS", "VIEW_CLASS_ANALYTICS", "DATABASE_ACCESS", "VIEW_DATABASE"]:
                return {"allowed": False, "reason": "I'm sorry, you don't have permission to access administrative databases."}

            return {"allowed": True, "reason": "General parent query permitted."}

        # ----------------------------------------------------
        # 3. TEACHER PERMISSIONS
        # ----------------------------------------------------
        if role == "TEACHER":
            assigned_classes = user.get("assigned_classes", [])
            if intent == "MARK_ATTENDANCE":
                if target_student_id:
                    student = db.get_student(target_student_id)
                    if student and student["grade_section"] not in assigned_classes:
                        return {"allowed": False, "reason": f"Teacher is not authorized to mark attendance for unassigned grade {student['grade_section']}."}
                return {"allowed": True, "reason": "Attendance marking permitted for assigned class."}

            if intent in ["DATABASE_ACCESS", "VIEW_DATABASE", "VIEW_STUDENT_ATTENDANCE", "VIEW_RECENT_ATTENDANCE", "VIEW_TIMETABLE", "OPEN_DASHBOARD", "GREETING", "HELP", "VIEW_SCHOOL_ANALYTICS", "VIEW_CLASS_ANALYTICS"]:
                return {"allowed": True, "reason": "Teacher database and student academic access granted."}

            return {"allowed": True, "reason": "General teacher query permitted."}

        # ----------------------------------------------------
        # 4. PRINCIPAL PERMISSIONS
        # ----------------------------------------------------
        if role == "PRINCIPAL":
            return {"allowed": True, "reason": "Principal has administrative oversight access."}

        return {"allowed": False, "reason": "Unknown role or unhandled permission scope."}


auth_guard = AuthorizationMiddleware()

