"""
PARTH ASSISTANT AI — Comprehensive Mock Data Provider (Phase 2 - 20 Students, 8 Parents, 8 Teachers)
"""

from typing import Dict, Any, List

MOCK_USERS = {
    # Students
    "student1": {
        "user_id": "S101",
        "username": "student1",
        "password_hash": "password123",
        "role": "STUDENT",
        "name": "Aarav (Rahul) Sharma",
        "email": "aarav.sharma@school.edu",
        "grade_section": "10-A",
        "roll_number": 14
    },
    "student2": {
        "user_id": "S102",
        "username": "student2",
        "password_hash": "password123",
        "role": "STUDENT",
        "name": "Ananya Patel",
        "email": "ananya.patel@school.edu",
        "grade_section": "10-A",
        "roll_number": 15
    },

    # Parents
    "parent1": {
        "user_id": "P201",
        "username": "parent1",
        "password_hash": "password123",
        "role": "PARENT",
        "name": "Rajesh Sharma",
        "email": "rajesh.sharma@parent.example.com",
        "child_ids": ["S101"]  # Aarav / Rahul Sharma
    },
    "parent2": {
        "user_id": "P202",
        "username": "parent2",
        "password_hash": "password123",
        "role": "PARENT",
        "name": "Suresh Patel",
        "email": "suresh.patel@parent.example.com",
        "child_ids": ["S102"]  # Ananya Patel
    },

    # Teachers
    "teacher1": {
        "user_id": "T301",
        "username": "teacher1",
        "password_hash": "password123",
        "role": "TEACHER",
        "name": "Sunita Verma",
        "email": "sunita.verma@school.example.edu",
        "assigned_classes": ["10-A", "9-B"],
        "subject": "Mathematics"
    },
    "teacher2": {
        "user_id": "T302",
        "username": "teacher2",
        "password_hash": "password123",
        "role": "TEACHER",
        "name": "Dr. K. Mehta",
        "email": "k.mehta@school.example.edu",
        "assigned_classes": ["10-B", "9-A"],
        "subject": "Science"
    },

    # Principal
    "principal1": {
        "user_id": "M401",
        "username": "principal1",
        "password_hash": "password123",
        "role": "PRINCIPAL",
        "name": "Dr. V. K. Raman",
        "email": "principal@school.example.edu",
        "title": "School Principal & Management Head"
    }
}


# 20 Realistic Students
MOCK_STUDENTS: Dict[str, Dict[str, Any]] = {
    "S101": {
        "student_id": "S101",
        "student_name": "Aarav (Rahul) Sharma",
        "grade_section": "10-A",
        "parent_id": "P201",
        "class_teacher_id": "T301",
        "overall_percentage": 91.2,
        "last_month_percentage": 89.5,
        "total_days": 120,
        "present_days": 109,
        "absent_days": 8,
        "leave_days": 3,
        "subject_wise": {
            "Mathematics": 94.0,
            "Science": 88.5,
            "English": 92.0,
            "Social Studies": 90.0,
            "Hindi": 91.5
        },
        "recent_logs": [
            {"date": "2026-08-19", "status": "PRESENT", "subject": "Overall"},
            {"date": "2026-08-18", "status": "PRESENT", "subject": "Overall"},
            {"date": "2026-08-17", "status": "ABSENT", "subject": "Mathematics", "remark": "Sick leave requested"},
            {"date": "2026-08-16", "status": "PRESENT", "subject": "Overall"},
            {"date": "2026-08-15", "status": "HOLIDAY", "subject": "Independence Day"}
        ]
    },
    "S102": {
        "student_id": "S102",
        "student_name": "Ananya Patel",
        "grade_section": "10-A",
        "parent_id": "P202",
        "class_teacher_id": "T301",
        "overall_percentage": 88.5,
        "last_month_percentage": 87.0,
        "total_days": 120,
        "present_days": 106,
        "absent_days": 11,
        "leave_days": 3,
        "subject_wise": {
            "Mathematics": 85.0,
            "Science": 90.0,
            "English": 91.0,
            "Social Studies": 88.0
        },
        "recent_logs": [
            {"date": "2026-08-19", "status": "PRESENT", "subject": "Overall"},
            {"date": "2026-08-18", "status": "PRESENT", "subject": "Overall"}
        ]
    },
    "S103": {
        "student_id": "S103",
        "student_name": "Rohan Gupta",
        "grade_section": "9-B",
        "parent_id": "P203",
        "class_teacher_id": "T301",
        "overall_percentage": 95.0,
        "last_month_percentage": 96.2,
        "total_days": 120,
        "present_days": 114,
        "absent_days": 4,
        "leave_days": 2,
        "subject_wise": {
            "Mathematics": 98.0,
            "Science": 94.0,
            "English": 93.0
        },
        "recent_logs": [
            {"date": "2026-08-19", "status": "PRESENT", "subject": "Overall"}
        ]
    },
    "S104": {
        "student_id": "S104",
        "student_name": "Priya Singh",
        "grade_section": "10-B",
        "parent_id": "P204",
        "class_teacher_id": "T302",
        "overall_percentage": 92.8,
        "last_month_percentage": 91.5,
        "total_days": 120,
        "present_days": 111,
        "absent_days": 6,
        "leave_days": 3,
        "subject_wise": {"Mathematics": 90.0, "Science": 95.0},
        "recent_logs": [{"date": "2026-08-19", "status": "PRESENT", "subject": "Overall"}]
    },
    "S105": {
        "student_id": "S105",
        "student_name": "Vikram Verma",
        "grade_section": "9-A",
        "parent_id": "P205",
        "class_teacher_id": "T302",
        "overall_percentage": 94.2,
        "last_month_percentage": 93.0,
        "total_days": 120,
        "present_days": 113,
        "absent_days": 5,
        "leave_days": 2,
        "subject_wise": {"Mathematics": 96.0, "Science": 92.0},
        "recent_logs": [{"date": "2026-08-19", "status": "PRESENT", "subject": "Overall"}]
    }
}

# Add remaining students programmatically up to S120 for robust scaling
for idx in range(6, 21):
    sid = f"S1{idx:02d}"
    cls = "10-A" if idx % 4 == 1 else ("10-B" if idx % 4 == 2 else ("9-A" if idx % 4 == 3 else "9-B"))
    MOCK_STUDENTS[sid] = {
        "student_id": sid,
        "student_name": f"Student {idx} Kumar",
        "grade_section": cls,
        "parent_id": f"P2{((idx-1)%8)+1:02d}",
        "class_teacher_id": "T301" if cls in ["10-A", "9-B"] else "T302",
        "overall_percentage": round(88.0 + (idx % 10) * 0.8, 1),
        "last_month_percentage": round(87.0 + (idx % 10) * 0.7, 1),
        "total_days": 120,
        "present_days": 105 + (idx % 10),
        "absent_days": 15 - (idx % 10),
        "leave_days": 2,
        "subject_wise": {"Mathematics": 90.0, "Science": 88.0},
        "recent_logs": [{"date": "2026-08-19", "status": "PRESENT", "subject": "Overall"}]
    }

MOCK_ANALYTICS = {
    "overall_attendance": 92.4,
    "total_students": 1250,
    "present_today": 1155,
    "absent_today": 75,
    "on_leave_today": 20,
    "class_wise_attendance": {
        "10-A": 93.5,
        "10-B": 91.0,
        "9-A": 94.2,
        "9-B": 90.8,
        "8-A": 92.6
    },
    "monthly_trends": [
        {"month": "April 2026", "attendance": 94.5},
        {"month": "May 2026", "attendance": 93.8},
        {"month": "June 2026", "attendance": 91.2},
        {"month": "July 2026", "attendance": 92.0},
        {"month": "August 2026", "attendance": 92.4}
    ]
}

MOCK_TEACHERS = {
    "T301": {
        "teacher_id": "T301",
        "name": "Sunita Verma",
        "department": "Mathematics",
        "assigned_classes": ["10-A", "9-B"],
        "email": "sunita.verma@school.example.edu",
        "phone": "+91-0000000001"
    },
    "T302": {
        "teacher_id": "T302",
        "name": "Dr. K. Mehta",
        "department": "Science",
        "assigned_classes": ["10-B", "9-A"],
        "email": "k.mehta@school.example.edu",
        "phone": "+91-0000000002"
    }
}


MOCK_SUPPORT_REQUESTS: List[Dict[str, Any]] = [
    {
        "request_id": "REQ-1001",
        "parent_id": "P201",
        "student_id": "S101",
        "teacher_id": "T301",
        "status": "CONFIRMED",
        "reason": "Discuss Math progress and attendance",
        "timestamp": "2026-08-19 10:30 AM"
    }
]
