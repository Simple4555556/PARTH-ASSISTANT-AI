"""
PARTH ASSISTANT AI — Response Parser
Parses and validates LLM generation outputs into strict application-level schemas.
"""

from typing import Dict, Any, List, Optional


class ResponseParser:
    def parse_rag_response(
        self,
        raw_text: str,
        citations: List[Dict[str, Any]],
        language: str = "en",
        component: str = "policy-card"
    ) -> Dict[str, Any]:
        return {
            "success": True,
            "source": "RAG",
            "text": raw_text.strip(),
            "response": raw_text.strip(),
            "language": language,
            "citations": citations,
            "ui_action": "SHOW_COMPONENT",
            "component": component
        }

    def parse_hybrid_response(
        self,
        raw_text: str,
        citations: List[Dict[str, Any]],
        data: Dict[str, Any],
        language: str = "en",
        component: str = "attendance-card"
    ) -> Dict[str, Any]:
        return {
            "success": True,
            "source": "HYBRID",
            "text": raw_text.strip(),
            "response": raw_text.strip(),
            "language": language,
            "citations": citations,
            "data": data,
            "ui_action": "SHOW_COMPONENT",
            "component": component
        }


response_parser = ResponseParser()
