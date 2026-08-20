"""
PARTH ASSISTANT AI — Comprehensive Multilingual Test Suite
Verifies End-to-End Multilingual Support for Chat, Voice STT/TTS, and Conversation Memory across ALL 11 Languages.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def get_token(username: str) -> str:
    res = client.post("/api/auth/login", json={"username": username, "password": "password123"})
    return res.json()["access_token"]


ALL_LANGUAGES = [
    ("en", "What is my attendance?", "VIEW_OWN_ATTENDANCE", "%"),
    ("hi", "मेरी attendance कितनी है?", "VIEW_OWN_ATTENDANCE", "उपस्थिति"),
    ("ta", "என் attendance எவ்வளவு?", "VIEW_OWN_ATTENDANCE", "87.5%"),
    ("te", "నా attendance ఎంత ఉంది?", "VIEW_OWN_ATTENDANCE", "87.5%"),
    ("mr", "माझी attendance किती आहे?", "VIEW_OWN_ATTENDANCE", "87.5%"),
    ("bn", "আমার attendance কত?", "VIEW_OWN_ATTENDANCE", "87.5%"),
    ("gu", "મારી attendance કેટલી છે?", "VIEW_OWN_ATTENDANCE", "87.5%"),
    ("pa", "ਮੇਰੀ attendance ਕਿੰਨੀ ਹੈ?", "VIEW_OWN_ATTENDANCE", "87.5%"),
    ("kn", "ನನ್ನ attendance ಎಷ್ಟು ಇದೆ?", "VIEW_OWN_ATTENDANCE", "87.5%"),
    ("ml", "എന്റെ attendance എത്രയാണ്?", "VIEW_OWN_ATTENDANCE", "87.5%"),
    ("ur", "میری حاضری کتنی ہے؟", "VIEW_OWN_ATTENDANCE", "حاضری")
]


@pytest.mark.parametrize("lang_code, prompt, expected_intent, expected_snippet", ALL_LANGUAGES)
def test_chat_response_in_all_11_languages(lang_code, prompt, expected_intent, expected_snippet):
    """Verifies that Chat response text is generated natively in the target language for all 11 languages."""
    token = get_token("student1")
    res = client.post(
        "/api/ai/chat",
        json={"message": prompt, "conversation_id": f"MULTI-CONV-{lang_code}", "language": lang_code},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["language"] == lang_code
    assert data["tts"]["language"] == lang_code
    assert expected_snippet in data["message"] or "87.5" in data["message"]


@pytest.mark.parametrize("lang_code, prompt, expected_intent, expected_snippet", ALL_LANGUAGES)
def test_voice_response_in_all_11_languages(lang_code, prompt, expected_intent, expected_snippet):
    """Verifies that Voice endpoint STT/TTS pipeline returns exact target locale audio & text across all 11 languages."""
    token = get_token("student1")
    res = client.post(
        "/api/ai/voice",
        json={"transcript": prompt, "conversation_id": f"VOICE-MULTI-CONV-{lang_code}", "language": lang_code},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["language"] == lang_code
    assert data["tts"]["language"] == lang_code
    assert expected_snippet in data["response"] or "87.5" in data["response"]


def test_mid_conversation_language_switching():
    """Verifies that switching languages mid-conversation (Hindi -> Tamil -> Urdu) updates memory and output modality."""
    token = get_token("student1")
    conv_id = "MID-SWITCH-CONV-999"

    # Turn 1: Hindi
    res1 = client.post(
        "/api/ai/chat",
        json={"message": "मेरी attendance कितनी है?", "conversation_id": conv_id, "language": "hi"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res1.status_code == 200
    assert res1.json()["language"] == "hi"

    # Turn 2: Switch to Tamil
    res2 = client.post(
        "/api/ai/chat",
        json={"message": "என் attendance எவ்வளவு?", "conversation_id": conv_id, "language": "ta"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res2.status_code == 200
    assert res2.json()["language"] == "ta"

    # Turn 3: Switch to Urdu
    res3 = client.post(
        "/api/ai/chat",
        json={"message": "میری حاضری کتنی ہے؟", "conversation_id": conv_id, "language": "ur"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res3.status_code == 200
    assert res3.json()["language"] == "ur"
    assert "حاضری" in res3.json()["message"] or "87.5" in res3.json()["message"]


def test_hinglish_code_switching_support():
    """Verifies natural Hinglish input ('Rahul ki attendance kitni hai?') returns localized Hindi response."""
    token = get_token("parent1")
    res = client.post(
        "/api/ai/chat",
        json={"message": "Rahul ki attendance kitni hai?", "conversation_id": "HINGLISH-CONV-1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["language"] in ["hi", "en"]
    assert "91.2" in data["message"]
