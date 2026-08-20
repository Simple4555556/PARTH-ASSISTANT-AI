"""
PARTH ASSISTANT AI — RAG Service Orchestrator
Coordinates Document Ingestion, Semantic Vector Search, Role-Based Access Filtering, Anti-Hallucination, and Citations.
"""

import os
from typing import Dict, Any, List, Optional
from rag.ingestion.document_loader import document_loader
from rag.chunking.text_chunker import text_chunker
from rag.vectorstore.memory_vectorstore import vector_store
from rag.citations.citation_builder import citation_builder


class RAGService:
    def __init__(self, knowledge_base_dir: Optional[str] = None):
        if knowledge_base_dir is None:
            knowledge_base_dir = os.path.join(os.path.dirname(__file__), "knowledge_base")
        self.kb_dir = knowledge_base_dir
        self.is_initialized = False
        self.initialize_knowledge_base()

    def initialize_knowledge_base(self):
        """Loads and indexes all official school policy documents into the vector store."""
        if not os.path.exists(self.kb_dir):
            return

        documents = document_loader.load_directory(self.kb_dir)
        all_chunks = []
        for doc in documents:
            chunks = text_chunker.chunk_document(doc)
            all_chunks.extend(chunks)

        vector_store.add_documents(all_chunks)
        self.is_initialized = True

    def query(
        self,
        question: str,
        user_role: str = "STUDENT",
        top_k: int = 3,
        min_score: float = 0.10
    ) -> Dict[str, Any]:
        """
        Executes Role-Filtered Semantic RAG query.
        Returns grounded context, formatted citations, and relevance metrics.
        """
        if not self.is_initialized:
            self.initialize_knowledge_base()

        search_results = vector_store.search(
            query=question,
            top_k=top_k,
            role_filter=user_role,
            min_score=min_score
        )

        if not search_results:
            return {
                "success": False,
                "found": False,
                "question": question,
                "context": "",
                "answer": "I couldn't find that information in the school knowledge base. Would you like me to connect you with school management?",
                "citations": [],
                "top_score": 0.0,
                "chunks_retrieved": 0
            }

        top_chunk = search_results[0]
        context_snippets = [f"[{r['metadata'].get('title', 'Policy')}] {r['text']}" for r in search_results]
        combined_context = "\n\n".join(context_snippets)
        citations = citation_builder.format_citations(search_results)

        return {
            "success": True,
            "found": True,
            "question": question,
            "context": combined_context,
            "answer": top_chunk["text"],
            "title": top_chunk["metadata"].get("title", "School Policy"),
            "section": top_chunk["metadata"].get("section", "General"),
            "category": top_chunk["metadata"].get("category", "Policy"),
            "citations": citations,
            "top_score": top_chunk["score"],
            "chunks_retrieved": len(search_results)
        }


rag_service = RAGService()
