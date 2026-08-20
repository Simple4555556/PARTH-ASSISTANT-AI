"""
PARTH ASSISTANT AI — Citation Builder
Constructs clean, auditable citations without leaking internal vector or document database IDs.
"""

from typing import List, Dict, Any


class CitationBuilder:
    def format_citations(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        citations = []
        seen = set()

        for res in search_results:
            meta = res.get("metadata", {})
            title = meta.get("title", "School Policy")
            source = meta.get("source", "School Handbook")
            section = meta.get("section", "General")
            key = f"{title}-{section}"

            if key not in seen:
                seen.add(key)
                citations.append({
                    "title": title,
                    "source": source,
                    "section": section,
                    "category": meta.get("category", "Policy"),
                    "relevance_score": res.get("score", 1.0)
                })

        return citations


citation_builder = CitationBuilder()
