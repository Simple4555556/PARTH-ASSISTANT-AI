"""
PARTH ASSISTANT AI — RAG Agent
Specialized agent for School Knowledge Base queries, Policy retrieval, and Grounded LLM Response synthesis.
"""

from typing import Dict, Any, Optional
from rag.rag_service import rag_service
from llm.llmService import llm_service


class RAGAgent:
    def handle_query(
        self,
        question: str,
        user_identity: Dict[str, Any],
        language: str = "en",
        persona: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        role = user_identity.get("role", "STUDENT")

        # 1. Execute Role-Filtered RAG Retrieval
        rag_result = rag_service.query(
            question=question,
            user_role=role,
            top_k=3,
            min_score=0.10
        )

        # 2. Synthesize Grounded LLM Answer
        llm_response = llm_service.generate_rag_response(
            question=question,
            rag_result=rag_result,
            user_role=role,
            language=language,
            persona=persona
        )

        return {
            "success": rag_result.get("success", True),
            "found": rag_result.get("found", False),
            "source": "RAG",
            "text": llm_response["text"],
            "response": llm_response["response"],
            "citations": llm_response["citations"],
            "ui_action": "SHOW_COMPONENT",
            "component": "policy-card",
            "data": {
                "title": rag_result.get("title", "School Policy"),
                "section": rag_result.get("section", "General"),
                "category": rag_result.get("category", "Policy"),
                "citations": llm_response["citations"]
            }
        }


rag_agent = RAGAgent()
