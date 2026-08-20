"""
PARTH ASSISTANT AI — Prompt Manager
Constructs strictly grounded RAG and Hybrid prompts with anti-hallucination constraints.
"""

from typing import Dict, Any, List


class PromptManager:
    RAG_GROUNDING_TEMPLATE = """You are Parth Assistant AI, the official school AI assistant.
Answer the user's question accurately and concisely based SOLELY on the retrieved official school knowledge context below.
Never invent policies or hallucinate details not present in the context.

Retrieved Context:
{context}

User Question: {question}
User Role: {role}
Target Language: {language}

Instructions:
1. State the factual policy answer clearly.
2. If context does not contain the answer, politely state: "I couldn't find that information in the school knowledge base. Would you like me to connect you with school management?"
3. Respond directly in {language}.
"""

    HYBRID_TEMPLATE = """You are Parth Assistant AI.
Answer the user's question by synthesizing their live ERP personal record with the official school policy below.

Live ERP Data:
{erp_data}

Official School Policy Context:
{rag_context}

User Question: {question}
Target Language: {language}

Instructions:
1. Clearly compare the live record (e.g. current attendance) with the required minimum policy threshold (e.g. 75%).
2. Conclude with a direct verdict (e.g. eligible, warning, below requirement).
3. Respond in {language}.
"""

    def build_rag_prompt(self, question: str, context: str, role: str, language: str = "en") -> str:
        return self.RAG_GROUNDING_TEMPLATE.format(
            question=question,
            context=context,
            role=role,
            language=language
        )

    def build_hybrid_prompt(self, question: str, erp_data: str, rag_context: str, language: str = "en") -> str:
        return self.HYBRID_TEMPLATE.format(
            question=question,
            erp_data=erp_data,
            rag_context=rag_context,
            language=language
        )


prompt_manager = PromptManager()
