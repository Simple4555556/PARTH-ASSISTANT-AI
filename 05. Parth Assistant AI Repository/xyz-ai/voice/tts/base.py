"""
PARTH ASSISTANT AI — Abstract Text-to-Speech Provider Interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class TextToSpeechProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Synthesizes text to audio payload.
        Returns: { "success": bool, "audio_data": bytes|None, "language": str, "latency_ms": float }
        Phase 4: Browser-native SpeechSynthesis handles playback in frontend.
        Server-side returns synthesized text payload; frontend plays via Web Speech API.
        """
        pass
