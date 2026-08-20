"""
Entity Extraction Agent — Extracts entities like student_name, subject, date, status, class_name
"""

import re
from typing import Dict, Any


class EntityAgent:
    KNOWN_NAMES = ["rahul", "aarav", "ananya", "rohan", "priya", "vikram"]
    KNOWN_SUBJECTS = ["mathematics", "math", "science", "english", "social studies", "hindi"]
    KNOWN_CLASSES = ["10-a", "10-b", "9-a", "9-b", "grade 10", "grade 9"]

    def extract_entities(self, text: str) -> Dict[str, Any]:
        msg_lower = text.lower()
        entities = {}

        # ID extraction (e.g., S101, S102, S103)
        id_match = re.search(r'\b(s\d{3})\b', msg_lower)
        if id_match:
            entities["student_id"] = id_match.group(1).upper()

        # Name extraction
        for name in self.KNOWN_NAMES:
            if name in msg_lower:
                entities["student_name"] = name.capitalize()
                if name == "rahul" and "student_id" not in entities:
                    entities["student_id"] = "S101"
                break



        # Subject extraction
        for sub in self.KNOWN_SUBJECTS:
            if sub in msg_lower:
                entities["subject"] = "Mathematics" if sub in ["math", "mathematics"] else sub.capitalize()
                break

        # Class extraction
        for cls in self.KNOWN_CLASSES:
            if cls in msg_lower:
                entities["class_name"] = cls.upper()
                break

        # Date / Date Range
        if "last month" in msg_lower:
            entities["date_range"] = "last_month"
        elif "today" in msg_lower:
            entities["date"] = "today"
        elif "yesterday" in msg_lower:
            entities["date"] = "yesterday"

        # Status
        if "absent" in msg_lower:
            entities["attendance_status"] = "ABSENT"
        elif "present" in msg_lower:
            entities["attendance_status"] = "PRESENT"
        elif "leave" in msg_lower:
            entities["attendance_status"] = "LEAVE"

        return entities


entity_agent = EntityAgent()
