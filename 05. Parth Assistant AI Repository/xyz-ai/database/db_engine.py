"""
PARTH ASSISTANT AI — Decoupled Database & Persistence Engine
Supports JSON/In-Memory persistence with pluggable MongoDB/SQLAlchemy interfaces.
"""

from typing import Dict, Any, List, Optional
import copy
from backend.mock_data import MOCK_USERS, MOCK_STUDENTS, MOCK_ANALYTICS, MOCK_TEACHERS, MOCK_SUPPORT_REQUESTS


class DatabaseEngine:
    """In-Memory / Document Repository for School ERP Data."""
    
    def __init__(self):
        self.users = copy.deepcopy(MOCK_USERS)
        self.students = copy.deepcopy(MOCK_STUDENTS)
        self.analytics = copy.deepcopy(MOCK_ANALYTICS)
        self.teachers = copy.deepcopy(MOCK_TEACHERS)
        self.support_requests = copy.deepcopy(MOCK_SUPPORT_REQUESTS)

    # User operations
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return self.users.get(username)

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        for u in self.users.values():
            if u["user_id"] == user_id:
                return u
        return None

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        username = user_data["username"]
        if username in self.users:
            raise ValueError(f"Username '{username}' already registered.")
        self.users[username] = user_data
        return user_data


    # Student operations
    def get_student(self, student_id: str) -> Optional[Dict[str, Any]]:
        return self.students.get(student_id)

    def get_children_for_parent(self, parent_id: str) -> List[Dict[str, Any]]:
        parent = self.get_user_by_id(parent_id)
        if not parent or parent.get("role") != "PARENT":
            return []
        child_ids = parent.get("child_ids", [])
        return [self.students[cid] for cid in child_ids if cid in self.students]

    # Attendance operations
    def get_attendance(self, student_id: str) -> Optional[Dict[str, Any]]:
        student = self.get_student(student_id)
        if not student:
            return None
        return {
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "grade_section": student["grade_section"],
            "overall_percentage": student["overall_percentage"],
            "last_month_percentage": student["last_month_percentage"],
            "total_days": student["total_days"],
            "present_days": student["present_days"],
            "absent_days": student["absent_days"],
            "leave_days": student["leave_days"],
            "subject_wise": student["subject_wise"],
            "recent_logs": student["recent_logs"]
        }

    def get_recent_attendance(self, student_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        student = self.get_student(student_id)
        if not student:
            return []
        return student["recent_logs"][:limit]

    def mark_attendance(self, student_id: str, date: str, status: str, subject: str = "Overall", remarks: Optional[str] = None) -> Dict[str, Any]:
        student = self.get_student(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")
        
        status_upper = status.upper()
        log_entry = {
            "date": date,
            "status": status_upper,
            "subject": subject,
            "remark": remarks or "Marked via API"
        }
        
        # Insert log at top
        student["recent_logs"].insert(0, log_entry)
        
        # Recalculate basic days
        if status_upper == "PRESENT":
            student["present_days"] += 1
            student["total_days"] += 1
        elif status_upper == "ABSENT":
            student["absent_days"] += 1
            student["total_days"] += 1
        
        if student["total_days"] > 0:
            student["overall_percentage"] = round((student["present_days"] / student["total_days"]) * 100, 1)

        return {
            "student_id": student_id,
            "student_name": student["student_name"],
            "date": date,
            "status": status_upper,
            "new_overall_percentage": student["overall_percentage"]
        }

    # Analytics operations
    def get_school_analytics(self) -> Dict[str, Any]:
        return self.analytics

    def get_class_analytics(self, class_name: str) -> Dict[str, Any]:
        rate = self.analytics["class_wise_attendance"].get(class_name)
        if rate is None:
            raise ValueError(f"Class {class_name} not found in analytics database")
        return {
            "class_name": class_name,
            "attendance_rate": rate,
            "overall_school_average": self.analytics["overall_attendance"]
        }

    # Support operations
    def create_support_request(self, parent_id: str, student_id: str, teacher_id: str, reason: str) -> Dict[str, Any]:
        req_id = f"REQ-{len(self.support_requests) + 1001}"
        record = {
            "request_id": req_id,
            "parent_id": parent_id,
            "student_id": student_id,
            "teacher_id": teacher_id,
            "status": "SUBMITTED",
            "reason": reason,
            "timestamp": "2026-08-20 00:00:00"
        }
        self.support_requests.append(record)
        return record

    def get_support_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        for req in self.support_requests:
            if req["request_id"] == request_id:
                return req
        return None

    # Teacher operations
    def get_teacher(self, teacher_id: str) -> Optional[Dict[str, Any]]:
        return self.teachers.get(teacher_id)


# Global Database Instance
db = DatabaseEngine()
