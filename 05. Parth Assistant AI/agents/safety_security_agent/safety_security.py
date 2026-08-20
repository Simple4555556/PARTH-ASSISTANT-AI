"""
Safety & Security Agent — Protects against prompt injection, fake claims, & unauthorized data access
"""


class SafetySecurityAgent:
    PROMPT_INJECTION_KEYWORDS = [
        "ignore all previous",
        "system prompt",
        "system instructions",
        "developer prompts",
        "bypass security",
        "show me every student's attendance",
        "reveal all api keys",
        "api key",
        "jwt secret",
        "secret values",
        "show all student records"
    ]

    def inspect_request(self, text: str) -> dict:
        text_lower = text.lower()
        for kw in self.PROMPT_INJECTION_KEYWORDS:
            if kw in text_lower:
                return {
                    "is_safe": False,
                    "reason": f"Security violation detected: '{kw}' is prohibited."
                }
        return {"is_safe": True}
