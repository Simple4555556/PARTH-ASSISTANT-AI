"""
PARTH ASSISTANT AI — Document Loader for RAG Ingestion Pipeline
Loads Markdown, TXT, and JSON documents and extracts metadata headers.
"""

import os
import re
from typing import List, Dict, Any


class DocumentLoader:
    def load_file(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        metadata = {
            "source": os.path.basename(file_path),
            "file_path": file_path,
            "document_id": f"DOC-{os.path.splitext(os.path.basename(file_path))[0].upper()}",
            "title": os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").title(),
            "category": "General Knowledge",
            "visibility": ["STUDENT", "PARENT", "TEACHER", "PRINCIPAL"]
        }

        # Extract title from first # Header if present
        title_match = re.search(r"^#\s+(.+)$", raw_text, re.MULTILINE)
        if title_match:
            metadata["title"] = title_match.group(1).strip()

        # Extract metadata fields formatted as **Field**: Value
        doc_id_match = re.search(r"\*\*Document ID\*\*:\s*([^\n]+)", raw_text, re.IGNORECASE)
        if doc_id_match:
            metadata["document_id"] = doc_id_match.group(1).strip()

        cat_match = re.search(r"\*\*Category\*\*:\s*([^\n]+)", raw_text, re.IGNORECASE)
        if cat_match:
            metadata["category"] = cat_match.group(1).strip()

        vis_match = re.search(r"\*\*Visibility\*\*:\s*([^\n]+)", raw_text, re.IGNORECASE)
        if vis_match:
            vis_str = vis_match.group(1).strip()
            metadata["visibility"] = [v.strip().upper() for v in vis_str.split(",")]

        src_match = re.search(r"\*\*Source\*\*:\s*([^\n]+)", raw_text, re.IGNORECASE)
        if src_match:
            metadata["source"] = src_match.group(1).strip()

        return {
            "text": raw_text,
            "metadata": metadata
        }

    def load_directory(self, dir_path: str) -> List[Dict[str, Any]]:
        docs = []
        if not os.path.exists(dir_path):
            return docs

        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith((".md", ".txt", ".json")):
                    file_path = os.path.join(root, file)
                    docs.append(self.load_file(file_path))
        return docs


document_loader = DocumentLoader()
