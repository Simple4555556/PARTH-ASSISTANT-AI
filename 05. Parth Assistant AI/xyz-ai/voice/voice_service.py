"""
PARTH ASSISTANT AI — Voice Service Orchestrator
Coordinates STT → AI Brain → TTS pipeline with real latency tracking.
Internally reuses POST /api/ai/chat pipeline via SupervisorAgent.
"""

import time
import uuid
from typing import Dict, Any, Optional

from voice.stt.provider import stt_provider
from voice.tts.provider import tts_provider
from agents.supervisor_agent.supervisor import supervisor_agent
from backend.authorization.audit_logger import audit_logger


class VoiceService:
    """
    Voice orchestrator:
      Transcript → STT Normalization → SupervisorAgent → TTS Synthesis
    All authorization, RBAC, and ML-based intent detection happen inside SupervisorAgent.
    Voice is only an input/output modality — it never bypasses the AI brain.
    """

    def process_voice_request(
        self,
        session_user: Dict[str, Any],
        transcript: str,
        language: str = "en",
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:

        req_id = f"VOICE-{uuid.uuid4().hex[:6].upper()}"
        conv_id = conversation_id or f"VCONV-{uuid.uuid4().hex[:6].upper()}"
        total_start = time.time()

        # 1. STT Normalization
        stt_start = time.time()
        stt_result = stt_provider.transcribe(transcript, language=language)
        stt_ms = round((time.time() - stt_start) * 1000, 2)

        if not stt_result["success"]:
            return {
                "request_id": req_id,
                "conversation_id": conv_id,
                "success": False,
                "transcript": "",
                "response": stt_result.get("error", "No speech detected. Please try again."),
                "tts": {"success": False, "text": "", "locale": "en-IN"},
                "language": language,
                "intent": None,
                "latency": {"stt_ms": stt_ms, "ai_ms": 0, "api_ms": 0, "tts_ms": 0, "total_ms": stt_ms}
            }

        normalized_transcript = stt_result["transcript"]

        # 2. AI Brain — SupervisorAgent (same as text chat, full security pipeline)
        ai_start = time.time()
        ai_result = supervisor_agent.process_request(
            session_user=session_user,
            user_message=normalized_transcript,
            conversation_id=conv_id,
            language_preference=language
        )
        ai_ms = round((time.time() - ai_start) * 1000, 2)
        api_ms = ai_result.get("processing_time_ms", 0)

        response_text = ai_result.get("response", "")
        detected_lang = ai_result.get("language", language)

        # 3. TTS Synthesis
        tts_start = time.time()
        tts_result = tts_provider.synthesize(response_text, language=detected_lang)
        tts_ms = round((time.time() - tts_start) * 1000, 2)

        total_ms = round((time.time() - total_start) * 1000, 2)

        # Sanitized Audit Logging — never logs raw audio or credentials
        audit_logger.log_event(
            request_id=req_id,
            user_id=session_user.get("user_id", "UNKNOWN"),
            role=session_user.get("role", "UNKNOWN"),
            action="VOICE_CHAT",
            resource=ai_result.get("tool_used") or "NONE",
            result="ALLOWED" if ai_result.get("success") else "DENIED",
            extra_details={
                "language": detected_lang,
                "intent": ai_result.get("intent"),
                "stt_ms": stt_ms,
                "ai_ms": ai_ms,
                "tts_ms": tts_ms
            }
        )

        return {
            "request_id": req_id,
            "conversation_id": conv_id,
            "success": True,
            "transcript": normalized_transcript,
            "response": response_text,
            "message": response_text,
            "ui_action": ai_result.get("ui_action", "NONE"),
            "component": ai_result.get("component"),
            "data": ai_result.get("data", {}),
            "role": ai_result.get("role"),
            "tts": tts_result,
            "language": detected_lang,
            "intent": ai_result.get("intent"),
            "tool_used": ai_result.get("tool_used"),
            "persona": ai_result.get("persona"),
            "latency": {
                "stt_ms": stt_ms,
                "ai_ms": ai_ms,
                "api_ms": api_ms,
                "tts_ms": tts_ms,
                "total_ms": total_ms
            }
        }



voice_service = VoiceService()
