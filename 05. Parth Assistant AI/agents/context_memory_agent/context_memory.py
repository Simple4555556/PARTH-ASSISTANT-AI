"""
Context & Memory Agent — Maintains multi-turn conversation state per session
"""

from typing import Dict, Any, Optional, List


class ContextMemoryAgent:
    def __init__(self):
        self._conversations: Dict[str, Dict[str, Any]] = {}

    def get_context(self, conversation_id: str) -> Dict[str, Any]:
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = {
                "conversation_id": conversation_id,
                "language": "en",
                "recent_intents": [],
                "entities": {},
                "last_student": None,
                "last_subject": None,
                "last_date_range": None,
                "pending_escalation": False,
                "messages": []
            }
        return self._conversations[conversation_id]

    def update_context(self, conversation_id: str, intent: str, entities: Dict[str, Any], user_msg: str, ai_msg: str, language: Optional[str] = None):
        ctx = self.get_context(conversation_id)
        ctx["recent_intents"].append(intent)
        if language:
            ctx["language"] = language

        # Update last known entities
        if entities.get("student_name"):
            ctx["last_student"] = entities["student_name"]
            ctx["entities"]["student_name"] = entities["student_name"]
        if entities.get("subject"):
            ctx["last_subject"] = entities["subject"]
            ctx["entities"]["subject"] = entities["subject"]
        if entities.get("date_range"):
            ctx["last_date_range"] = entities["date_range"]
            ctx["entities"]["date_range"] = entities["date_range"]

        ctx["messages"].append({"user": user_msg, "ai": ai_msg})

    def set_language(self, conversation_id: str, language: str):
        ctx = self.get_context(conversation_id)
        ctx["language"] = language

    def get_language(self, conversation_id: str) -> str:
        ctx = self.get_context(conversation_id)
        return ctx.get("language", "en")


    def resolve_contextual_query(self, conversation_id: str, new_intent: str, new_entities: Dict[str, Any]) -> Dict[str, Any]:
        ctx = self.get_context(conversation_id)
        resolved_entities = new_entities.copy()

        # If student name is missing in query, carry over from last context
        if "student_name" not in resolved_entities and ctx.get("last_student"):
            resolved_entities["student_name"] = ctx["last_student"]

        # If date range is specified (e.g. "What about last month?"), update intent to VIEW_RECENT_ATTENDANCE
        if resolved_entities.get("date_range") == "last_month" and new_intent in ["VIEW_CHILD_ATTENDANCE", "VIEW_OWN_ATTENDANCE", "UNKNOWN"]:
            resolved_intent = "VIEW_RECENT_ATTENDANCE"
        else:
            resolved_intent = new_intent

        return {
            "intent": resolved_intent,
            "entities": resolved_entities,
            "last_student": ctx.get("last_student"),
            "pending_escalation": ctx.get("pending_escalation", False)
        }

    def set_pending_escalation(self, conversation_id: str, status: bool):
        ctx = self.get_context(conversation_id)
        ctx["pending_escalation"] = status


context_memory_agent = ContextMemoryAgent()
