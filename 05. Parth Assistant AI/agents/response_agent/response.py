"""
Response Agent — Converts structured tool outcomes into human-like persona responses
"""

from typing import Dict, Any


class ResponseAgent:
    def format_response(
        self,
        intent: str,
        user: Dict[str, Any],
        persona: Dict[str, Any],
        tool_result: Dict[str, Any],
        auth_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        name = user.get("name", "User")
        role = user.get("role", "STUDENT")

        # 1. Handle authorization refusal
        if not auth_result.get("allowed"):
            reason = auth_result.get("reason", "")
            if intent in ["DATABASE_ACCESS", "VIEW_DATABASE"]:
                msg = "I'm sorry, you don't have permission to access the database."
            else:
                msg = f"I'm sorry {name}, you don't have permission to access that information."
            return {
                "message": msg,
                "ui_action": "NONE",
                "component": None,
                "data": {}
            }

        # 2. Handle tool errors / API failures
        if not tool_result.get("success") and "error" in tool_result:
            return {
                "message": f"I'm unable to process that request right now: {tool_result['error']}",
                "ui_action": "NONE",
                "component": None,
                "data": {}
            }

        # 3. Intent specific responses & contextual UI mappings
        if intent in ["VIEW_OWN_ATTENDANCE", "VIEW_CHILD_ATTENDANCE", "VIEW_STUDENT_ATTENDANCE"]:
            data = tool_result.get("data", {})
            pct = data.get("overall_percentage", 87.5)
            student_name = data.get("student_name", "Rahul" if role == "PARENT" else name)
            present_days = data.get("present_days", 35)
            absent_days = data.get("absent_days", 5)
            total_days = data.get("total_days", 40)

            if role == "STUDENT":
                msg = f"Your current attendance is {pct}%."
            elif role == "PARENT":
                msg = f"Here is {student_name}'s current attendance."
            else:
                msg = f"{student_name}'s attendance is {pct}%."

            return {
                "message": msg,
                "ui_action": "SHOW_COMPONENT",
                "component": "attendance-card",
                "data": {
                    "student_id": data.get("student_id", "S101"),
                    "student_name": student_name,
                    "overall_percentage": pct,
                    "present_days": present_days,
                    "absent_days": absent_days,
                    "total_days": total_days
                }
            }

        if intent == "VIEW_RECENT_ATTENDANCE":
            logs = tool_result.get("logs") or tool_result.get("data", {}).get("recent_logs", [])
            if not logs:
                logs = [
                    {"date": "Aug 20", "subject": "Mathematics", "status": "PRESENT"},
                    {"date": "Aug 19", "subject": "Science", "status": "PRESENT"},
                    {"date": "Aug 18", "subject": "English", "status": "ABSENT"},
                    {"date": "Aug 17", "subject": "Computer", "status": "PRESENT"}
                ]
            student_name = tool_result.get("data", {}).get("student_name", "Rahul" if role == "PARENT" else name)
            return {
                "message": f"Here is {student_name}'s recent attendance.",
                "ui_action": "SHOW_COMPONENT",
                "component": "recent-attendance",
                "data": {
                    "student_name": student_name,
                    "recent_logs": logs
                }
            }

        if intent == "MARK_ATTENDANCE":
            data = tool_result.get("data", {})
            student_name = data.get("student_name", "Rahul")
            status = data.get("status", "ABSENT")
            date = data.get("date", "Today")
            already_marked = tool_result.get("success", False) and "message" in tool_result

            if already_marked:
                msg = f"{student_name} has been marked {status.lower()} today."
            else:
                msg = f"Please confirm attendance mark for {student_name}."

            return {
                "message": msg,
                "ui_action": "OPEN_MODAL" if not already_marked else "SHOW_COMPONENT",
                "component": "mark-attendance",
                "data": {
                    "student_id": data.get("student_id", "S101"),
                    "student_name": student_name,
                    "date": date,
                    "status": status,
                    "confirmed": already_marked
                }
            }

        if intent in ["VIEW_SCHOOL_ANALYTICS", "VIEW_CLASS_ANALYTICS"]:
            data = tool_result.get("data", {})
            overall = data.get("overall_attendance", 88.7)
            present = data.get("present_today", 4320)
            absent = data.get("absent_today", 550)
            total = data.get("total_students", present + absent)
            return {
                "message": f"Overall school attendance is {overall}%.",
                "ui_action": "SHOW_CHART",
                "component": "attendance-analytics",
                "data": {
                    "overall_attendance": overall,
                    "present_today": present,
                    "absent_today": absent,
                    "total_students": total,
                    "class_wise": data.get("class_wise_attendance", {"10-A": 93.5, "10-B": 89.2, "9-A": 86.4})
                }
            }

        if intent in ["DATABASE_ACCESS", "VIEW_DATABASE"]:
            if role == "TEACHER":
                return {
                    "message": "Opening the student database view.",
                    "ui_action": "SHOW_TABLE",
                    "component": "student-database",
                    "data": {
                        "students": [
                            {"id": "STU001", "name": "Rahul Sharma", "grade": "10-A", "attendance": 91.2, "status": "Active"},
                            {"id": "STU002", "name": "Aman Verma", "grade": "10-B", "attendance": 86.4, "status": "Active"},
                            {"id": "STU003", "name": "Priya Patel", "grade": "10-A", "attendance": 94.1, "status": "Active"},
                            {"id": "STU004", "name": "Karan Singh", "grade": "9-A", "attendance": 88.0, "status": "Active"}
                        ]
                    }
                }
            return {
                "message": "Opening school database.",
                "ui_action": "OPEN_PAGE",
                "component": "database-view",
                "data": {
                    "collections": [
                        {"name": "Students", "count": 120},
                        {"name": "Parents", "count": 85},
                        {"name": "Teachers", "count": 24},
                        {"name": "Attendance", "count": 8420},
                        {"name": "Classes", "count": 12},
                        {"name": "Subjects", "count": 36}
                    ]
                }
            }


        if intent == "VIEW_TIMETABLE":
            return {
                "message": f"Here is the class timetable.",
                "ui_action": "SHOW_COMPONENT",
                "component": "timetable-card",
                "data": {
                    "grade_section": "Class 10-A",
                    "schedule": [
                        {"period": "Period 1 (08:30 - 09:15)", "subject": "Mathematics", "teacher": "Mr. Sharma"},
                        {"period": "Period 2 (09:15 - 10:00)", "subject": "Science", "teacher": "Mrs. Sunita"},
                        {"period": "Period 3 (10:15 - 11:00)", "subject": "English", "teacher": "Ms. Ananya"},
                        {"period": "Period 4 (11:00 - 11:45)", "subject": "Computer Science", "teacher": "Mr. Verma"}
                    ]
                }
            }

        if intent == "VIEW_TEACHERS":
            return {
                "message": "Here is the list of teachers.",
                "ui_action": "SHOW_TABLE",
                "component": "teacher-list",
                "data": {
                    "teachers": [
                        {"name": "Sunita Verma", "subject": "Science & Class Teacher", "email": "sunita@school.edu"},
                        {"name": "Ramesh Kumar", "subject": "Mathematics", "email": "ramesh@school.edu"},
                        {"name": "Ananya Roy", "subject": "English", "email": "ananya@school.edu"}
                    ]
                }
            }

        if intent in ["CONTACT_TEACHER", "CONTACT_MANAGEMENT"]:
            return {
                "message": "I can submit a call request to your child's teacher.",
                "ui_action": "SHOW_FORM",
                "component": "support-request",
                "data": tool_result.get("data", {})
            }

        if intent == "OPEN_DASHBOARD":
            return {
                "message": "Opening complete dashboard.",
                "ui_action": "OPEN_PAGE",
                "component": "full-dashboard",
                "data": {"role": role}
            }

        if intent == "GREETING":
            prefix = persona.get("greeting_prefix", "Hello")
            title = persona.get("name", "Assistant")
            return {
                "message": f"Hi, I'm Parth Assistant AI.\nHow can I help you today?",
                "ui_action": "NONE",
                "component": None,
                "data": {}
            }

        return {
            "message": f"Hello {name}! How can I assist you today?",
            "ui_action": "NONE",
            "component": None,
            "data": {}
        }


response_agent = ResponseAgent()

