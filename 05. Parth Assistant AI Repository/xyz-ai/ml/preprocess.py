"""
PARTH ASSISTANT AI — ML Preprocessing Module
Tokenization, lowercasing, and text normalization.
"""

import re


def preprocess_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    # Remove punctuation except alphanumeric and spaces
    text = re.sub(r"[^\w\s]", "", text)
    # Strip multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text
