"""
PARTH ASSISTANT AI — TTS Provider Implementation
Phase 4: Returns text for browser-native SpeechSynthesis playback.
Phase 5+: Can be swapped for server-rendered audio (Google Cloud TTS, Azure TTS, etc.)
"""

import time
from typing import Dict, Any
from voice.tts.base import TextToSpeechProvider

LANGUAGE_VOICE_MAP = {
    "en": "en-IN",
    "hi": "hi-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "mr": "mr-IN",
    "bn": "bn-IN",
    "gu": "gu-IN",
    "pa": "pa-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "ur": "ur-IN"
}


class BrowserTTSProvider(TextToSpeechProvider):
    """
    Provides text + locale for browser-native SpeechSynthesis API.
    Audio playback is handled by the frontend via window.speechSynthesis.
    """

    def synthesize(self, text: str, language: str = "en") -> Dict[str, Any]:
        start = time.time()

        if not text or not text.strip():
            return {
                "success": False,
                "text": "",
                "locale": "en-IN",
                "language": language,
                "error": "No text to speak.",
                "latency_ms": round((time.time() - start) * 1000, 2)
            }

        locale = LANGUAGE_VOICE_MAP.get(language, "en-IN")

        return {
            "success": True,
            "text": text,
            "locale": locale,
            "language": language,
            "latency_ms": round((time.time() - start) * 1000, 2)
        }


class FallbackTTSProvider(TextToSpeechProvider):
    """Fallback when browser TTS is unavailable — returns silent success."""

    def synthesize(self, text: str, language: str = "en") -> Dict[str, Any]:
        return {
            "success": False,
            "text": text,
            "locale": LANGUAGE_VOICE_MAP.get(language, "en-IN"),
            "language": language,
            "error": "TTS unavailable. Response text is shown in chat.",
            "latency_ms": 0.0
        }


tts_provider = BrowserTTSProvider()
fallback_tts = FallbackTTSProvider()
