"""
PARTH ASSISTANT AI — Voice Chat API Router (POST /api/ai/voice)
Reuses the full AI brain pipeline via VoiceService.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .auth import get_current_user
from .authorization.rate_limiter import rate_limiter
from voice.voice_service import voice_service


class VoicePayload(BaseModel):
    transcript: str
    conversation_id: Optional[str] = None
    language: Optional[str] = "en"


router = APIRouter(prefix="/api/ai", tags=["AI Voice Brain"])


@router.post("/voice", summary="Parth Assistant AI Voice Input Endpoint")
def voice_endpoint(
    payload: VoicePayload,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Accepts a speech transcript (from browser Web Speech API or client STT).
    Enforces rate limiting & JWT authentication.
    Routes through VoiceService → SupervisorAgent (same full security pipeline as /chat).
    Returns structured AI response + TTS synthesis payload for frontend playback.
    """
    if not payload.transcript or not payload.transcript.strip():
        raise HTTPException(
            status_code=400,
            detail="No speech was detected. Please try again."
        )

    # Rate Limiting Check (same guard as /chat)
    rate_limiter.check_rate_limit(current_user["user_id"])

    result = voice_service.process_voice_request(
        session_user=current_user,
        transcript=payload.transcript,
        language=payload.language or "en",
        conversation_id=payload.conversation_id
    )

    return {
        "conversation_id": result["conversation_id"],
        "transcript": result["transcript"],
        "message": result["response"],
        "response": result["response"],
        "ui_action": result.get("ui_action", "NONE"),
        "component": result.get("component"),
        "data": result.get("data", {}),
        "intent": result["intent"],
        "language": result["language"],
        "role": result.get("role", current_user.get("role")),
        "tool_used": result.get("tool_used"),
        "persona": result.get("persona"),
        "tts": result["tts"],
        "latency": result["latency"],
        "success": result["success"]
    }

