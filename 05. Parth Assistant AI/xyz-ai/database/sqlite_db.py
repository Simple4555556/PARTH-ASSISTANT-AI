"""
PARTH ASSISTANT AI — SQLite Relational Database Engine for School ERP
Provides structured schema, relational integrity, and analytical SQL queries.
"""

import sqlite3
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "school_erp.db")


class SQLiteDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. School Info
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS school_info (
                school_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                pincode TEXT NOT NULL,
                board TEXT NOT NULL,
                established_year INTEGER NOT NULL
            )
            """)

            # 2. Classes
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                class_id TEXT PRIMARY KEY,
                class_name TEXT NOT NULL,
                section TEXT NOT NULL,
                academic_year TEXT NOT NULL,
                class_teacher_id TEXT,
                room_number TEXT NOT NULL,
                capacity INTEGER NOT NULL DEFAULT 40,
                student_count INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'ACTIVE'
            )
            """)

            # 3. Parents
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS parents (
                parent_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                relationship TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                pincode TEXT NOT NULL,
                occupation TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE'
            )
            """)

            # 4. Teachers
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id TEXT PRIMARY KEY,
                employee_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                department TEXT NOT NULL,
                designation TEXT NOT NULL,
                subjects TEXT NOT NULL,
                classes TEXT NOT NULL,
                joining_date TEXT NOT NULL,
                experience_years INTEGER NOT NULL,
                qualification TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE'
            )
            """)

            # 5. Students
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                admission_number TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                class_id TEXT NOT NULL,
                class_name TEXT NOT NULL,
                section TEXT NOT NULL,
                roll_number INTEGER NOT NULL,
                parent_id TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                pincode TEXT NOT NULL,
                admission_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                academic_year TEXT NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (parent_id) REFERENCES parents(parent_id)
            )
            """)

            # 6. Subjects
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id TEXT PRIMARY KEY,
                subject_name TEXT NOT NULL,
                class_id TEXT NOT NULL,
                class_name TEXT NOT NULL,
                subject_code TEXT NOT NULL,
                teacher_id TEXT NOT NULL,
                maximum_marks INTEGER NOT NULL DEFAULT 100,
                passing_marks INTEGER NOT NULL DEFAULT 35,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
            )
            """)

            # 7. Teacher-Class Assignments
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS teacher_classes (
                assignment_id TEXT PRIMARY KEY,
                teacher_id TEXT NOT NULL,
                class_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                academic_year TEXT NOT NULL,
                periods_per_week INTEGER NOT NULL DEFAULT 5,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            )
            """)

            # 8. Attendance (1-Week Full Dataset + Subject Wise)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                class_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                teacher_id TEXT NOT NULL,
                date TEXT NOT NULL,
                day TEXT NOT NULL,
                status TEXT NOT NULL,
                marked_at TEXT NOT NULL,
                marked_by TEXT NOT NULL,
                remarks TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
            )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_att_student ON attendance(student_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_att_date ON attendance(date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_att_class ON attendance(class_id)")

            # 9. Exams
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                exam_id TEXT PRIMARY KEY,
                exam_name TEXT NOT NULL,
                exam_type TEXT NOT NULL,
                academic_year TEXT NOT NULL,
                class_id TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'COMPLETED'
            )
            """)

            # 10. Marks
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                mark_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                class_id TEXT NOT NULL,
                exam_id TEXT NOT NULL,
                exam_name TEXT NOT NULL,
                marks_obtained REAL NOT NULL,
                maximum_marks REAL NOT NULL DEFAULT 100.0,
                percentage REAL NOT NULL,
                grade TEXT NOT NULL,
                result TEXT NOT NULL,
                exam_date TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (exam_id) REFERENCES exams(exam_id)
            )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_marks_student ON marks(student_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_marks_subject ON marks(subject_id)")

            # 11. Timetable
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable (
                timetable_id TEXT PRIMARY KEY,
                class_id TEXT NOT NULL,
                section TEXT NOT NULL,
                day TEXT NOT NULL,
                period INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                teacher_id TEXT NOT NULL,
                room_number TEXT NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
            )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tt_teacher_slot ON timetable(teacher_id, day, period)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tt_class_slot ON timetable(class_id, day, period)")

            # 12. Class Sessions (Teacher Activity)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS class_sessions (
                session_id TEXT PRIMARY KEY,
                teacher_id TEXT NOT NULL,
                class_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                date TEXT NOT NULL,
                period INTEGER NOT NULL,
                status TEXT NOT NULL,
                topic TEXT NOT NULL,
                attendance_marked INTEGER NOT NULL DEFAULT 1,
                remarks TEXT,
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            )
            """)

            # 13. Leave Requests
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_requests (
                leave_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                parent_id TEXT NOT NULL,
                leave_type TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                approved_by TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (parent_id) REFERENCES parents(parent_id)
            )
            """)

            # 14. Fees
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS fees (
                fee_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                academic_year TEXT NOT NULL,
                fee_type TEXT NOT NULL,
                amount REAL NOT NULL,
                due_date TEXT NOT NULL,
                paid_amount REAL NOT NULL DEFAULT 0.0,
                payment_date TEXT,
                status TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
            """)

            # 15. Assignments
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                assignment_id TEXT PRIMARY KEY,
                teacher_id TEXT NOT NULL,
                class_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                assigned_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            )
            """)

            # 16. Announcements
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                announcement_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                created_by TEXT NOT NULL,
                audience TEXT NOT NULL,
                created_at TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'NORMAL',
                status TEXT NOT NULL DEFAULT 'ACTIVE'
            )
            """)

            # 17. Support Requests
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS support_requests (
                request_id TEXT PRIMARY KEY,
                created_by TEXT NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                created_at TEXT NOT NULL,
                resolved_at TEXT
            )
            """)

            # 18. Users (Auth table)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                child_ids TEXT,
                assigned_classes TEXT,
                grade_section TEXT,
                subject TEXT,
                phone TEXT
            )
            """)
            conn.commit()

    # Query Helpers
    def query_one(self, sql: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def query_all(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def execute(self, sql: str, params: tuple = ()) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount

    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(sql, params_list)
            conn.commit()
            return cursor.rowcount


sqlite_db = SQLiteDB()
