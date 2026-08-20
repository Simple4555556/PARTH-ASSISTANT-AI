"""
PARTH ASSISTANT AI — Memory VectorStore
High-performance Cosine-Similarity Vector Database with deterministic Role-Based Access Filtering.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from rag.vectorstore.base import BaseVectorStore
from rag.embeddings.embedding_service import embedding_service


class MemoryVectorStore(BaseVectorStore):
    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None

    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        if not documents:
            return 0

        self.chunks.extend(documents)
        all_texts = [c["text"] for c in self.chunks]
        # Re-fit and embed
        embedding_service.fit_corpus(all_texts)
        self.embeddings = embedding_service.embed_texts(all_texts)
        return len(documents)

    def search(
        self,
        query: str,
        top_k: int = 4,
        role_filter: Optional[str] = None,
        min_score: float = 0.12
    ) -> List[Dict[str, Any]]:
        if not self.chunks or self.embeddings is None:
            return []

        query_vec = embedding_service.embed_query(query)
        # Cosine similarity dot product on normalized vectors
        scores = np.dot(self.embeddings, query_vec)

        results = []
        for idx, score in enumerate(scores):
            if score < min_score:
                continue

            chunk = self.chunks[idx]
            metadata = chunk.get("metadata", {})
            visibility = metadata.get("visibility", ["STUDENT", "PARENT", "TEACHER", "PRINCIPAL"])

            # Strict Role-Based Retrieval Access Control
            if role_filter:
                role_upper = role_filter.upper()
                if role_upper not in [v.upper() for v in visibility]:
                    continue

            results.append({
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "score": float(round(score, 4)),
                "metadata": metadata
            })

        # Sort by descending similarity score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def delete(self, document_id: str) -> bool:
        initial_count = len(self.chunks)
        self.chunks = [c for c in self.chunks if c.get("metadata", {}).get("document_id") != document_id]
        if len(self.chunks) < initial_count:
            if self.chunks:
                all_texts = [c["text"] for c in self.chunks]
                self.embeddings = embedding_service.embed_texts(all_texts)
            else:
                self.embeddings = None
            return True
        return False

    def update(self, document_id: str, new_document: Dict[str, Any]) -> bool:
        self.delete(document_id)
        self.add_documents([new_document])
        return True

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "provider": "MemoryVectorStore",
            "total_chunks": len(self.chunks),
            "vector_dimension": self.embeddings.shape[1] if self.embeddings is not None else 0
        }


vector_store = MemoryVectorStore()
