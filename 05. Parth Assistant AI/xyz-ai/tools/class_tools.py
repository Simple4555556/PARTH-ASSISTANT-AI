"""
PARTH ASSISTANT AI — Class Tools
Provides class directory lookups and roster details.
"""

from typing import Dict, Any, List
from database.sqlite_db import sqlite_db


class ClassTools:
    def get_all_classes(self) -> Dict[str, Any]:
        classes = sqlite_db.query_all("SELECT * FROM classes ORDER BY class_name")
        return {"success": True, "classes": classes}

    def get_class_students(self, class_id: str) -> Dict[str, Any]:
        students = sqlite_db.query_all(
            "SELECT student_id, admission_number, name, roll_number, gender FROM students WHERE class_id = ? OR class_name = ? ORDER BY roll_number",
            (class_id, class_id)
        )
        return {"success": True, "class_id": class_id, "students": students}


class_tools = ClassTools()
