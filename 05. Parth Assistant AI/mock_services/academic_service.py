"""
PARTH ASSISTANT AI — Academic & Operations Service
Handles Exams, Marks, Timetable, Assignments, Fees, and Leave Requests from SQLite database.
"""

from typing import Dict, Any, List, Optional
from database.sqlite_db import sqlite_db


class AcademicService:
    # ── Marks & Exam Analytics ───────────────────────────────────────────
    def get_student_marks(self, student_id: str, exam_name: Optional[str] = None) -> List[Dict[str, Any]]:
        if exam_name:
            sql = "SELECT * FROM marks WHERE student_id = ? AND exam_name = ? ORDER BY exam_date DESC"
            return sqlite_db.query_all(sql, (student_id, exam_name))
        sql = "SELECT * FROM marks WHERE student_id = ? ORDER BY exam_date DESC"
        return sqlite_db.query_all(sql, (student_id,))

    def get_subject_results(self, subject_name: str, class_name: Optional[str] = None) -> Dict[str, Any]:
        if class_name:
            sql = """
            SELECT m.* FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            WHERE s.subject_name LIKE ? AND s.class_name = ?
            """
            rows = sqlite_db.query_all(sql, (f"%{subject_name}%", class_name))
        else:
            sql = """
            SELECT m.* FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            WHERE s.subject_name LIKE ?
            """
            rows = sqlite_db.query_all(sql, (f"%{subject_name}%",))

        if not rows:
            return {
                "subject": subject_name,
                "class_name": class_name or "ALL",
                "total_students": 0,
                "passed": 0,
                "failed": 0,
                "pass_percentage": 0.0,
                "average_marks": 0.0,
                "highest_marks": 0.0,
                "lowest_marks": 0.0
            }

        total = len(rows)
        passed = sum(1 for r in rows if r["result"] == "PASS")
        failed = total - passed
        scores = [r["marks_obtained"] for r in rows]
        
        return {
            "subject": subject_name,
            "class_name": class_name or "ALL",
            "total_students": total,
            "passed": passed,
            "failed": failed,
            "pass_percentage": round((passed / total) * 100, 1) if total else 0.0,
            "average_marks": round(sum(scores) / total, 1) if total else 0.0,
            "highest_marks": max(scores) if scores else 0.0,
            "lowest_marks": min(scores) if scores else 0.0
        }

    def get_school_results_summary(self) -> Dict[str, Any]:
        sql = "SELECT marks_obtained, result FROM marks"
        rows = sqlite_db.query_all(sql)
        total = len(rows)
        passed = sum(1 for r in rows if r["result"] == "PASS")
        scores = [r["marks_obtained"] for r in rows]

        return {
            "total_exam_records": total,
            "total_passed": passed,
            "total_failed": total - passed,
            "overall_pass_rate": round((passed / total) * 100, 1) if total else 0.0,
            "average_score": round(sum(scores) / total, 1) if total else 0.0
        }

    # ── Timetable ────────────────────────────────────────────────────────
    def get_class_timetable(self, class_id: str, day: Optional[str] = None) -> List[Dict[str, Any]]:
        if day:
            sql = """
            SELECT t.*, s.subject_name, tc.name as teacher_name
            FROM timetable t
            JOIN subjects s ON t.subject_id = s.subject_id
            JOIN teachers tc ON t.teacher_id = tc.teacher_id
            WHERE t.class_id = ? AND LOWER(t.day) = LOWER(?)
            ORDER BY t.period ASC
            """
            return sqlite_db.query_all(sql, (class_id, day))
        
        sql = """
        SELECT t.*, s.subject_name, tc.name as teacher_name
        FROM timetable t
        JOIN subjects s ON t.subject_id = s.subject_id
        JOIN teachers tc ON t.teacher_id = tc.teacher_id
        WHERE t.class_id = ?
        ORDER BY CASE t.day 
            WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 WHEN 'Saturday' THEN 6 ELSE 7 END,
            t.period ASC
        """
        return sqlite_db.query_all(sql, (class_id,))

    def get_teacher_timetable(self, teacher_id: str, day: Optional[str] = None) -> List[Dict[str, Any]]:
        if day:
            sql = """
            SELECT t.*, s.subject_name, c.class_name
            FROM timetable t
            JOIN subjects s ON t.subject_id = s.subject_id
            JOIN classes c ON t.class_id = c.class_id
            WHERE t.teacher_id = ? AND LOWER(t.day) = LOWER(?)
            ORDER BY t.period ASC
            """
            return sqlite_db.query_all(sql, (teacher_id, day))
        
        sql = """
        SELECT t.*, s.subject_name, c.class_name
        FROM timetable t
        JOIN subjects s ON t.subject_id = s.subject_id
        JOIN classes c ON t.class_id = c.class_id
        WHERE t.teacher_id = ?
        ORDER BY t.period ASC
        """
        return sqlite_db.query_all(sql, (teacher_id,))

    # ── Fees ─────────────────────────────────────────────────────────────
    def get_student_fees(self, student_id: str) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM fees WHERE student_id = ? ORDER BY due_date ASC"
        return sqlite_db.query_all(sql, (student_id,))

    def get_school_fee_summary(self) -> Dict[str, Any]:
        sql = "SELECT amount, paid_amount, status FROM fees"
        rows = sqlite_db.query_all(sql)
        total_billed = sum(r["amount"] for r in rows)
        total_collected = sum(r["paid_amount"] for r in rows)
        return {
            "total_billed": total_billed,
            "total_collected": total_collected,
            "total_pending": total_billed - total_collected,
            "collection_rate": round((total_collected / total_billed) * 100, 1) if total_billed else 0.0
        }

    # ── Assignments ──────────────────────────────────────────────────────
    def get_class_assignments(self, class_id: str) -> List[Dict[str, Any]]:
        sql = """
        SELECT a.*, s.subject_name, t.name as teacher_name
        FROM assignments a
        JOIN subjects s ON a.subject_id = s.subject_id
        JOIN teachers t ON a.teacher_id = t.teacher_id
        WHERE a.class_id = ?
        ORDER BY a.due_date ASC
        """
        return sqlite_db.query_all(sql, (class_id,))

    # ── Leave Requests ───────────────────────────────────────────────────
    def get_student_leaves(self, student_id: str) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM leave_requests WHERE student_id = ? ORDER BY start_date DESC"
        return sqlite_db.query_all(sql, (student_id,))

    # ── Announcements ────────────────────────────────────────────────────
    def get_announcements(self, audience: Optional[str] = None) -> List[Dict[str, Any]]:
        if audience and audience != "ALL":
            sql = "SELECT * FROM announcements WHERE audience = 'ALL' OR audience = ? ORDER BY created_at DESC"
            return sqlite_db.query_all(sql, (audience,))
        sql = "SELECT * FROM announcements ORDER BY created_at DESC"
        return sqlite_db.query_all(sql)


academic_service = AcademicService()
