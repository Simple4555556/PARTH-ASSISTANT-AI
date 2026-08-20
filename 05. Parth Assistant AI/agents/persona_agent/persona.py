"""
Persona Agent — Manages persona configuration and role-adapted tone
"""

from typing import Dict, Any


class PersonaAgent:
    PERSONAS = {
        "STUDENT": {
            "name": "Academic Assistant",
            "tone": "Friendly, encouraging, supportive",
            "greeting_prefix": "Hi"
        },
        "PARENT": {
            "name": "Parent Support Assistant",
            "tone": "Caring, patient, reassuring",
            "greeting_prefix": "Hello"
        },
        "TEACHER": {
            "name": "Teaching Assistant",
            "tone": "Professional, efficient, helpful",
            "greeting_prefix": "Hello"
        },
        "PRINCIPAL": {
            "name": "Management Assistant",
            "tone": "Professional, concise, analytical",
            "greeting_prefix": "Respected"
        }
    }

    def get_persona(self, role: str) -> Dict[str, Any]:
        return self.PERSONAS.get(role, self.PERSONAS["STUDENT"])


persona_agent = PersonaAgent()
