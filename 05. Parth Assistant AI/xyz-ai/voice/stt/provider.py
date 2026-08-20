"""
PARTH ASSISTANT AI — STT Provider Implementation
Handles server-side transcript normalization for 11 Indian Languages + Hinglish.
"""

import time
from typing import Any, Dict
from voice.stt.base import SpeechToTextProvider


class DefaultSTTProvider(SpeechToTextProvider):
    """
    Primary STT provider.
    Phase 4 uses browser Web Speech API for transcription.
    This provider normalizes and validates the transcript received from the browser.
    In future phases, swap with Whisper / Google Cloud STT by swapping this class.
    """

    SUPPORTED_LANGUAGES = ["en", "hi", "ta", "te", "mr", "bn", "gu", "pa", "kn", "ml", "ur"]

    def transcribe(self, audio_bytes_or_transcript: Any, language: str = "en") -> Dict[str, Any]:
        start = time.time()

        if not audio_bytes_or_transcript:
            return {
                "success": False,
                "transcript": "",
                "language": language,
                "error": "No speech detected. Please try again.",
                "latency_ms": round((time.time() - start) * 1000, 2)
            }

        transcript = str(audio_bytes_or_transcript).strip()

        if not transcript:
            return {
                "success": False,
                "transcript": "",
                "language": language,
                "error": "No speech was detected. Please try again.",
                "latency_ms": round((time.time() - start) * 1000, 2)
            }

        return {
            "success": True,
            "transcript": transcript,
            "language": language if language in self.SUPPORTED_LANGUAGES else "en",
            "latency_ms": round((time.time() - start) * 1000, 2)
        }


stt_provider = DefaultSTTProvider()
