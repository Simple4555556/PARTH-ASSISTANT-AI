"""
PARTH ASSISTANT AI — Browser STT Handler (Web Speech API)
Handles browser-native speech recognition with graceful fallback messaging.
"""

LANGUAGE_MAP = {
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

# Browser STT is handled in the frontend (React) via Web Speech API.
# This module documents the expected behavior and language codes for the browser.

BROWSER_STT_SUPPORTED_LANGUAGES = list(LANGUAGE_MAP.keys())


def get_browser_locale(lang_code: str) -> str:
    """Return the BCP-47 locale string for Web Speech API."""
    return LANGUAGE_MAP.get(lang_code, "en-IN")


FALLBACK_MESSAGE = (
    "Voice input is not supported in this browser. Please use text input."
)
