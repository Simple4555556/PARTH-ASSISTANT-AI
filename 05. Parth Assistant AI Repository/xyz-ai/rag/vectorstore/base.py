"""
PARTH ASSISTANT AI — VectorStore Abstract Base Class
Provides a standard pluggable interface for Vector Database implementations (FAISS, Chroma, Qdrant, Memory).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        """Indexes document chunks into the vector store."""
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 4,
        role_filter: Optional[str] = None,
        min_score: float = 0.15
    ) -> List[Dict[str, Any]]:
        """Performs semantic similarity search with role-based access filtering."""
        pass

    @abstractmethod
    def delete(self, document_id: str) -> bool:
        """Deletes all chunks belonging to a document."""
        pass

    @abstractmethod
    def update(self, document_id: str, new_document: Dict[str, Any]) -> bool:
        """Updates document chunks."""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Returns vector database health and index statistics."""
        pass
