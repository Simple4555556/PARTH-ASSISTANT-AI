"""
PARTH ASSISTANT AI — Abstract Speech-to-Text Provider Interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class SpeechToTextProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes_or_transcript: Any, language: str = "en") -> Dict[str, Any]:
        """
        Transcribes audio data or normalizes spoken transcript.
        Returns: { "success": bool, "transcript": str, "language": str, "latency_ms": float }
        """
        pass
