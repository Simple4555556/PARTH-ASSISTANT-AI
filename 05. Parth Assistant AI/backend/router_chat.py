"""
PARTH ASSISTANT AI — Chat API Router (POST /api/ai/chat - Phase 3 Multilingual & Rate Limited)
"""

import time
import uuid
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from .auth import get_current_user
from .authorization.rate_limiter import rate_limiter
from agents.supervisor_agent.supervisor import supervisor_agent


class ChatPayload(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    language: Optional[str] = "en"


router = APIRouter(prefix="/api/ai", tags=["AI Chat Brain"])


@router.post("/chat", summary="Parth Assistant AI Brain Chat Endpoint")
def chat_endpoint(payload: ChatPayload, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Receives user message and optional language code.
    Derives authenticated identity directly from JWT token session.
    Enforces rate limiting and routes request through SupervisorAgent.
    Tracks precise execution latency with unique request UUID.
    """
    t_req_received = time.time()
    req_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"

    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Rate Limiting Check
    rate_limiter.check_rate_limit(current_user["user_id"])

    res = supervisor_agent.process_request(
        session_user=current_user,
        user_message=payload.message,
        conversation_id=payload.conversation_id,
        language_preference=payload.language,
        request_id=req_id,
        t_req_received=t_req_received
    )

    return {
        "success": res.get("success", True),
        "request_id": res.get("request_id", req_id),
        "conversation_id": res["conversation_id"],
        "message": res["response"],
        "response": res["response"],
        "text": res["response"],
        "ui_action": res.get("ui_action", "NONE"),
        "component": res.get("component"),
        "data": res.get("data", {}),
        "intent": res["intent"],
        "language": res.get("language", "en"),
        "detected_language": res.get("detected_language", "en"),
        "tts": res.get("tts", {"enabled": True, "language": res.get("language", "en")}),
        "tool_used": res["tool_used"],
        "role": res["role"],
        "persona": res["persona"],
        "timing_breakdown": res.get("timing_breakdown", {}),
        "processing_time_ms": res.get("processing_time_ms", 0.0)
    }
