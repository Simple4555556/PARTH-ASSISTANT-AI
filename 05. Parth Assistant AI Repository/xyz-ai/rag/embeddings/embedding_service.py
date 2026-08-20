"""
PARTH ASSISTANT AI — Embedding Service
Computes dense L2-normalized vector embeddings for multilingual policy documents and user queries.
"""

from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class EmbeddingService:
    def __init__(self):
        # Character & Word Subword N-Gram Vectorizer for cross-lingual & native script semantic capture
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
            sublinear_tf=True
        )
        self.is_fitted = False

    def fit_corpus(self, texts: List[str]):
        """Fits the embedding vocabulary on the document corpus."""
        if not texts:
            return
        self.vectorizer.fit(texts)
        self.is_fitted = True

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embeds a list of document chunk texts into normalized dense vectors."""
        if not self.is_fitted:
            self.fit_corpus(texts)
        matrix = self.vectorizer.transform(texts).toarray()
        # L2-normalize
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return matrix / norms

    def embed_query(self, query: str) -> np.ndarray:
        """Embeds a single query into a normalized vector."""
        if not self.is_fitted:
            self.fit_corpus([query])
        vec = self.vectorizer.transform([query]).toarray()[0]
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec


embedding_service = EmbeddingService()
