"""
PARTH ASSISTANT AI — Text Chunking Pipeline
Splits structured school knowledge documents into semantic chunks with overlap and metadata.
"""

import re
from typing import List, Dict, Any


class TextChunker:
    def __init__(self, chunk_size: int = 450, chunk_overlap: int = 60):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        raw_text = document.get("text", "")
        doc_metadata = document.get("metadata", {})
        doc_id = doc_metadata.get("document_id", "DOC")

        # Split into sections based on ## headers or double newlines
        sections = re.split(r"\n(?=##\s+)", raw_text)
        chunks = []
        chunk_idx = 1

        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue

            # Extract section heading if present
            sec_heading = "General"
            heading_match = re.match(r"^##\s+(.+)$", sec, re.MULTILINE)
            if heading_match:
                sec_heading = heading_match.group(1).strip()

            # Clean markdown metadata block from first section
            cleaned_sec = re.sub(r"\*\*[^*]+\*\*:[^\n]+\n?", "", sec).strip()

            if len(cleaned_sec) <= self.chunk_size:
                chunks.append({
                    "chunk_id": f"{doc_id}_CH{chunk_idx:02d}",
                    "text": cleaned_sec,
                    "metadata": {
                        **doc_metadata,
                        "chunk_id": f"{doc_id}_CH{chunk_idx:02d}",
                        "section": sec_heading,
                        "char_count": len(cleaned_sec)
                    }
                })
                chunk_idx += 1
            else:
                # Sliding window split for long sections
                start = 0
                while start < len(cleaned_sec):
                    end = min(start + self.chunk_size, len(cleaned_sec))
                    chunk_text = cleaned_sec[start:end].strip()
                    if chunk_text:
                        chunks.append({
                            "chunk_id": f"{doc_id}_CH{chunk_idx:02d}",
                            "text": f"[{sec_heading}] {chunk_text}",
                            "metadata": {
                                **doc_metadata,
                                "chunk_id": f"{doc_id}_CH{chunk_idx:02d}",
                                "section": sec_heading,
                                "char_count": len(chunk_text)
                            }
                        })
                        chunk_idx += 1
                    start += self.chunk_size - self.chunk_overlap

        return chunks


text_chunker = TextChunker()
