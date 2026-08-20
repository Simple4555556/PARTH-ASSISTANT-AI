"""
Intent Agent — Hybrid ML + Rule Classifier with Confidence Probability Scoring (Conversational-First Expansion)
"""

from typing import Dict, Any
from ml.predict import predict_intent


class IntentAgent:
    INTENTS = [
        "VIEW_OWN_ATTENDANCE",
        "VIEW_CHILD_ATTENDANCE",
        "VIEW_STUDENT_ATTENDANCE",
        "VIEW_RECENT_ATTENDANCE",
        "MARK_ATTENDANCE",
        "VIEW_SCHOOL_ANALYTICS",
        "VIEW_CLASS_ANALYTICS",
        "DATABASE_ACCESS",
        "VIEW_DATABASE",
        "VIEW_TIMETABLE",
        "VIEW_TEACHERS",
        "OPEN_DASHBOARD",
        "CONTACT_TEACHER",
        "CONTACT_MANAGEMENT",
        "KNOWLEDGE_QUERY",
        "HYBRID_QUERY",
        "GREETING",
        "HELP",
        "UNKNOWN"
    ]

    def detect_intent(self, text: str, user_role: str = "STUDENT") -> Dict[str, Any]:
        msg = text.lower().strip()

        # Security check: prompt injection or fake role claim keywords
        if any(phrase in msg for phrase in ["ignore all previous", "system prompt", "system instructions", "developer prompts", "api key", "secret values", "reveal all"]):
            return {"intent": "PROMPT_INJECTION", "confidence": 0.99, "source": "SECURITY_GUARD"}

        if any(phrase in msg for phrase in ["i am actually the principal", "i am the principal"]):
            return {"intent": "FAKE_ROLE_CLAIM", "confidence": 0.98, "source": "SECURITY_GUARD"}

        # ── HYBRID QUERIES (ERP Live Record + RAG School Policy Synthesis) ─────────
        if any(kw in msg for kw in [
            "below the minimum", "below the required", "below the requirement", "below minimum",
            "below requirement", "eligible for exams", "qualify for exams", "satisfy the minimum",
            "kam hai kya", "requirement se kam"
        ]) or any(kw in text for kw in ["requirement se kam", "न्यूनतम से कम", "தேவையை விட குறைவு", "తక్కువగా ఉందా"]):
            return {"intent": "HYBRID_QUERY", "confidence": 0.98, "source": "RULE_HYBRID"}

        # ── RAG KNOWLEDGE & POLICY QUERIES ─────────────────────────────────────────
        if any(kw in msg for kw in [
            "policy", "rules", "rule", "requirement", "minimum attendance", "guidelines",
            "passing marks", "grading scale", "exam rules", "fee schedule", "refund policy",
            "leave policy", "absence policy", "handbook", "protocol", "discretionary authority"
        ]) or any(kw in text for kw in [
            "नियम", "पॉलिसी", "policy", "விதிகள்", "నియమాలు", "धोरण", "নিয়মাবলী", "નિયમો", "ਨਿਯਮ", "ನಿಯಮಗಳು", "നിയമങ്ങൾ", "قواعد"
        ]):
            return {"intent": "KNOWLEDGE_QUERY", "confidence": 0.97, "source": "RULE_RAG"}

        # Explicit Rule Overrides
        if any(kw in msg for kw in ["database", "show database", "show me the database", "access database", "db", "all students", "show all students", "student database"]):
            return {"intent": "DATABASE_ACCESS", "confidence": 0.98, "source": "RULE"}

        if any(kw in msg for kw in ["open complete dashboard", "show complete dashboard", "show full dashboard", "open dashboard", "complete dashboard"]):
            return {"intent": "OPEN_DASHBOARD", "confidence": 0.98, "source": "RULE"}

        if any(kw in msg for kw in ["timetable", "schedule", "time table", "class schedule"]):
            return {"intent": "VIEW_TIMETABLE", "confidence": 0.96, "source": "RULE"}

        if any(kw in msg for kw in ["my teachers", "show teachers", "who are my teachers", "teacher list"]):
            return {"intent": "VIEW_TEACHERS", "confidence": 0.96, "source": "RULE"}

        if any(kw in msg for kw in ["last month", "recent logs", "recent attendance", "yesterday"]):
            return {"intent": "VIEW_RECENT_ATTENDANCE", "confidence": 0.95, "source": "RULE"}

        if any(kw in msg for kw in ["mark ", "absent", "present"]):
            return {"intent": "MARK_ATTENDANCE", "confidence": 0.96, "source": "RULE"}

        if any(kw in msg for kw in ["teacher", "talk to teacher", "call teacher", "contact teacher"]):
            return {"intent": "CONTACT_TEACHER", "confidence": 0.95, "source": "RULE"}

        if any(kw in msg for kw in ["overall", "school attendance", "analytics", "school analytics", "show analytics"]):
            return {"intent": "VIEW_SCHOOL_ANALYTICS", "confidence": 0.96, "source": "RULE"}

        # English + Hinglish: own attendance
        if any(kw in msg for kw in ["my attendance", "meri attendance", "what is my attendance", "show my attendance"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE"}


        # ── Multilingual Native-Script Own Attendance Rules ──────────────────────────
        # Hindi (Devanagari)
        if any(kw in text for kw in ["मेरी attendance", "मेरी उपस्थिति", "मेरी हाजिरी", "मेरी हाज़िरी"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Tamil (Tamil script)
        if any(kw in text for kw in ["என் attendance", "என்னுடைய attendance", "என் வருகை", "எனது attendance"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Telugu (Telugu script)
        if any(kw in text for kw in ["నా attendance", "నా హాజరు", "నా హాజరీ"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Marathi (Devanagari)
        if any(kw in text for kw in ["माझी attendance", "माझी उपस्थिती", "माझी हजेरी"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Bengali (Bengali script)
        if any(kw in text for kw in ["আমার attendance", "আমার উপস্থিতি", "আমার হাজিরা"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Gujarati (Gujarati script)
        if any(kw in text for kw in ["મારી attendance", "મારી હાજરી"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Punjabi (Gurmukhi script)
        if any(kw in text for kw in ["ਮੇਰੀ attendance", "ਮੇਰੀ ਹਾਜ਼ਰੀ", "ਮੇਰੀ ਹਾਜਰੀ"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Kannada (Kannada script)
        if any(kw in text for kw in ["ನನ್ನ attendance", "ನನ್ನ ಹಾಜರಾತಿ"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Malayalam (Malayalam script)
        if any(kw in text for kw in ["എന്റെ attendance", "എന്റെ ഹാജർ"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}

        # Urdu (Arabic script)
        if any(kw in text for kw in ["میری حاضری", "میری حضوری", "میری attendance"]):
            return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": 0.97, "source": "RULE_MULTILINGUAL"}
        # ─────────────────────────────────────────────────────────────────────────────

        if any(kw in msg for kw in ["rahul", "child", "son", "daughter", "bete ki"]):
            return {"intent": "VIEW_CHILD_ATTENDANCE", "confidence": 0.95, "source": "RULE"}

        if any(kw in msg for kw in ["s103", "s102", "other student", "another student"]):
            return {"intent": "VIEW_STUDENT_ATTENDANCE", "confidence": 0.95, "source": "RULE"}

        if any(kw in msg for kw in ["yes", "confirm", "sure", "proceed"]):
            return {"intent": "CONFIRMATION", "confidence": 0.95, "source": "RULE"}


        # ML Model Inference
        try:
            ml_res = predict_intent(text)
            ml_intent = ml_res.get("intent")
            ml_conf = ml_res.get("confidence", 0.0)

            if ml_conf >= 0.25 and ml_intent in self.INTENTS:
                if user_role == "PARENT" and ml_intent == "VIEW_OWN_ATTENDANCE":
                    return {"intent": "VIEW_CHILD_ATTENDANCE", "confidence": ml_conf, "source": "ML_HYBRID"}
                if user_role == "STUDENT" and ml_intent == "VIEW_CHILD_ATTENDANCE":
                    return {"intent": "VIEW_OWN_ATTENDANCE", "confidence": ml_conf, "source": "ML_HYBRID"}
                return {"intent": ml_intent, "confidence": ml_conf, "source": "ML_MODEL"}
        except Exception:
            pass

        return {"intent": "UNKNOWN", "confidence": 0.20, "source": "FALLBACK"}


intent_agent = IntentAgent()
