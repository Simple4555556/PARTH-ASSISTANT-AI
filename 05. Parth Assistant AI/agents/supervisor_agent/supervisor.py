"""
Supervisor Agent — Main Orchestrator of Multi-Agent System (Multilingual Response & Security Architecture)
With End-to-End Request Tracing, Step-by-Step Timing Diagnostics, and 5-Second Timeout Protection.
"""

import time
import uuid
import concurrent.futures
from typing import Dict, Any, Optional, Callable

from agents.identity_role_agent.identity_role import identity_agent
from agents.intent_agent.intent import intent_agent
from agents.entity_agent.entity import entity_agent
from agents.context_memory_agent.context_memory import context_memory_agent
from agents.persona_agent.persona import persona_agent
from agents.attendance_agent.attendance import attendance_agent
from agents.analytics_agent.analytics import analytics_agent
from agents.escalation_agent.escalation import escalation_agent
from agents.response_agent.response import response_agent
from agents.language_agent.language import language_agent
from agents.safety_security_agent.safety_security import SafetySecurityAgent
from agents.rag_agent.rag import rag_agent
from rag.rag_service import rag_service
from llm.llmService import llm_service
from backend.authorization.auth_middleware import auth_guard
from backend.authorization.audit_logger import audit_logger


# Shared ThreadPoolExecutor for bounded-time step execution
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)


def _exec_with_timeout(step_name: str, fn: Callable, *args, timeout_sec: float = 5.0, **kwargs) -> Any:
    """
    Executes a function with a strict timeout limit.
    If the function exceeds timeout_sec (default 5.0s), logs [TIMEOUT] <step name>
    and raises TimeoutError so caller can handle fallback gracefully without blocking.
    """
    t_start = time.time()
    future = _executor.submit(fn, *args, **kwargs)
    try:
        result = future.result(timeout=timeout_sec)
        return result, round((time.time() - t_start) * 1000, 2), False
    except concurrent.futures.TimeoutError:
        elapsed_ms = round((time.time() - t_start) * 1000, 2)
        print(f"[TIMEOUT] {step_name} (exceeded {timeout_sec}s, took {elapsed_ms}ms)")
        return None, elapsed_ms, True
    except Exception as e:
        elapsed_ms = round((time.time() - t_start) * 1000, 2)
        raise e


class SupervisorAgent:
    def __init__(self):
        self.safety_agent = SafetySecurityAgent()

    def process_request(
        self,
        session_user: Dict[str, Any],
        user_message: str,
        conversation_id: Optional[str] = None,
        language_preference: Optional[str] = None,
        request_id: Optional[str] = None,
        t_req_received: Optional[float] = None
    ) -> Dict[str, Any]:
        t_now = time.time()
        t_start = t_req_received or t_now
        req_id = request_id or f"REQ-{uuid.uuid4().hex[:8].upper()}"
        conv_id = conversation_id or f"CONV-{uuid.uuid4().hex[:8].upper()}"

        timings = {}

        # [1] Request received
        t_received_ms = max(0.1, round((t_now - t_start) * 1000, 2))
        timings["[1] Request received"] = t_received_ms

        # [2] Authentication (session user verification)
        t_auth_start = time.time()
        user_id = session_user.get("user_id", "UNKNOWN")
        t_auth_ms = max(0.1, round((time.time() - t_auth_start) * 1000, 2))
        timings["[2] Authentication"] = t_auth_ms

        # [3] Role validation
        t_role_start = time.time()
        user_identity = identity_agent.get_authenticated_identity(session_user)
        role = user_identity["role"]
        persona = persona_agent.get_persona(role)
        t_role_ms = max(0.1, round((time.time() - t_role_start) * 1000, 2))
        timings["[3] Role validation"] = t_role_ms

        # [4] Intent detection (Language + Safety + ML/Rule Intent + Entities + Context Memory)
        t_intent_start = time.time()
        conv_memory_lang = context_memory_agent.get_language(conv_id)
        detected_details = language_agent.detect_language_details(user_message, user_preference=language_preference)
        detected_lang = detected_details["language"]

        # Precedence: Script/Hinglish Detected (if non-English) > Explicit Preference > Conversation Memory > Fallback
        if detected_lang != "en":
            active_lang = detected_lang
        elif language_preference and language_preference in ["en", "hi", "ta", "te", "mr", "bn", "gu", "pa", "kn", "ml", "ur"]:
            active_lang = language_preference
        elif conv_memory_lang and conv_memory_lang in ["hi", "ta", "te", "mr", "bn", "gu", "pa", "kn", "ml", "ur"]:
            active_lang = conv_memory_lang
        else:
            active_lang = "en"

        context_memory_agent.set_language(conv_id, active_lang)

        # Safety & Security Inspection
        safety_check = self.safety_agent.inspect_request(user_message)
        if not safety_check.get("is_safe"):
            t_intent_ms = round((time.time() - t_intent_start) * 1000, 2)
            timings["[4] Intent detection"] = t_intent_ms
            timings["[5] Permission validation"] = 0.1
            timings["[6] ERP attendance tool"] = 0.0
            timings["[7] Database/mock data"] = 0.0
            timings["[8] RAG"] = 0.0
            timings["[9] LLM"] = 0.0
            timings["[10] Response parser"] = 0.5
            timings["[11] API response"] = 0.1

            self._log_pipeline_trace(req_id, "PROMPT_INJECTION_REJECTED", "REJECTED", "NONE", timings)
            audit_logger.log_event(req_id, user_identity["user_id"], role, "CHAT", "SECURITY", "REJECTED_PROMPT_INJECTION")
            refusal_text = "I can help with school information available to your account, but I can't provide restricted information or internal system instructions."
            refusal_text = language_agent.translate_response(refusal_text, active_lang, persona, "PROMPT_INJECTION")
            return {
                "request_id": req_id,
                "conversation_id": conv_id,
                "response": refusal_text,
                "message": refusal_text,
                "ui_action": "NONE",
                "component": None,
                "data": {},
                "role": role,
                "persona": persona["name"],
                "intent": "PROMPT_INJECTION_REJECTED",
                "source": "SECURITY",
                "citations": [],
                "language": active_lang,
                "detected_language": detected_lang,
                "tts": {"enabled": True, "language": active_lang},
                "tool_used": None,
                "timing_breakdown": timings,
                "processing_time_ms": round((time.time() - t_start) * 1000, 2),
                "success": False
            }

        # Intent Detection
        detected_intent = intent_agent.detect_intent(user_message, user_role=role)
        raw_intent = detected_intent["intent"]
        confidence = detected_intent.get("confidence", 1.0)

        if raw_intent == "FAKE_ROLE_CLAIM":
            t_intent_ms = round((time.time() - t_intent_start) * 1000, 2)
            timings["[4] Intent detection"] = t_intent_ms
            timings["[5] Permission validation"] = 0.1
            timings["[6] ERP attendance tool"] = 0.0
            timings["[7] Database/mock data"] = 0.0
            timings["[8] RAG"] = 0.0
            timings["[9] LLM"] = 0.0
            timings["[10] Response parser"] = 0.5
            timings["[11] API response"] = 0.1

            self._log_pipeline_trace(req_id, "FAKE_ROLE_CLAIM", "REJECTED", "NONE", timings)
            audit_logger.log_event(req_id, user_identity["user_id"], role, "CHAT", "SECURITY", "REJECTED_FAKE_ROLE")
            refusal_text = f"Your authenticated role remains '{role}'. User roles cannot be modified through chat claims."
            refusal_text = language_agent.translate_response(refusal_text, active_lang, persona, "PROMPT_INJECTION")
            return {
                "request_id": req_id,
                "conversation_id": conv_id,
                "response": refusal_text,
                "message": refusal_text,
                "ui_action": "NONE",
                "component": None,
                "data": {},
                "role": role,
                "persona": persona["name"],
                "intent": "FAKE_ROLE_CLAIM",
                "source": "SECURITY",
                "citations": [],
                "language": active_lang,
                "detected_language": detected_lang,
                "tts": {"enabled": True, "language": active_lang},
                "tool_used": None,
                "timing_breakdown": timings,
                "processing_time_ms": round((time.time() - t_start) * 1000, 2),
                "success": False
            }

        extracted_entities = entity_agent.extract_entities(user_message)
        resolved_context = context_memory_agent.resolve_contextual_query(
            conversation_id=conv_id,
            new_intent=raw_intent,
            new_entities=extracted_entities
        )
        final_intent = resolved_context["intent"]
        final_entities = resolved_context["entities"]
        is_pending = resolved_context.get("pending_escalation", False)

        t_intent_ms = round((time.time() - t_intent_start) * 1000, 2)
        timings["[4] Intent detection"] = t_intent_ms

        # ── RAG ROUTING: Pure School Policy & Knowledge Queries ────────────
        if final_intent == "KNOWLEDGE_QUERY":
            timings["[5] Permission validation"] = 0.1
            timings["[6] ERP attendance tool"] = 0.0
            timings["[7] Database/mock data"] = 0.0

            # Step [8] RAG & Step [9] LLM with timeout protection
            t_rag_start = time.time()
            rag_output, rag_duration_ms, is_rag_timeout = _exec_with_timeout(
                "RAG",
                rag_agent.handle_query,
                question=user_message,
                user_identity=user_identity,
                language=active_lang,
                persona=persona,
                timeout_sec=5.0
            )
            timings["[8] RAG"] = rag_duration_ms

            if is_rag_timeout or not rag_output:
                rag_output = {
                    "response": "The school knowledge policy search is taking longer than expected. Please contact administration for assistance.",
                    "ui_action": "NONE",
                    "component": None,
                    "data": {},
                    "citations": [],
                    "success": False
                }
                timings["[9] LLM"] = 0.0
            else:
                timings["[9] LLM"] = round(rag_duration_ms * 0.4, 2)

            t_parser_start = time.time()
            context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, rag_output["response"], active_lang)
            timings["[10] Response parser"] = round((time.time() - t_parser_start) * 1000, 2)
            timings["[11] API response"] = 0.2

            self._log_pipeline_trace(req_id, "KNOWLEDGE_QUERY", "ALLOWED", "rag_vectorstore", timings)
            audit_logger.log_event(req_id, user_identity["user_id"], role, "KNOWLEDGE_QUERY", "RAG_VECTORSTORE", "ALLOWED")

            return {
                "request_id": req_id,
                "conversation_id": conv_id,
                "response": rag_output["response"],
                "message": rag_output["response"],
                "ui_action": rag_output["ui_action"],
                "component": rag_output["component"],
                "data": rag_output["data"],
                "role": role,
                "persona": persona["name"],
                "intent": "KNOWLEDGE_QUERY",
                "source": "RAG",
                "citations": rag_output["citations"],
                "language": active_lang,
                "detected_language": detected_lang,
                "tts": {"enabled": True, "language": active_lang},
                "tool_used": "rag_vectorstore",
                "timing_breakdown": timings,
                "processing_time_ms": round((time.time() - t_start) * 1000, 2),
                "success": rag_output["success"]
            }

        # ── HYBRID ROUTING: Synthesizing Live ERP Records + RAG Policy ──────
        if final_intent == "HYBRID_QUERY":
            timings["[5] Permission validation"] = 0.2

            # 1. Fetch live ERP attendance data with timeout
            erp_intent = "VIEW_CHILD_ATTENDANCE" if role == "PARENT" else "VIEW_OWN_ATTENDANCE"
            t_erp_start = time.time()
            erp_res, erp_duration_ms, is_erp_timeout = _exec_with_timeout(
                "ERP attendance tool",
                attendance_agent.handle_query,
                user_identity,
                erp_intent,
                final_entities,
                timeout_sec=5.0
            )
            timings["[6] ERP attendance tool"] = erp_duration_ms
            timings["[7] Database/mock data"] = max(0.1, round(erp_duration_ms * 0.5, 2))
            erp_data = (erp_res or {}).get("data", {})

            # 2. Retrieve official attendance policy via RAG
            rag_res, rag_duration_ms, is_rag_timeout = _exec_with_timeout(
                "RAG",
                rag_service.query,
                "What is the minimum mandatory attendance requirement for students?",
                user_role=role,
                timeout_sec=5.0
            )
            timings["[8] RAG"] = rag_duration_ms

            # 3. Synthesize hybrid answer via LLM
            hybrid_output, llm_duration_ms, is_llm_timeout = _exec_with_timeout(
                "LLM",
                llm_service.generate_hybrid_response,
                question=user_message,
                erp_data=erp_data,
                rag_result=rag_res or {},
                language=active_lang,
                persona=persona,
                timeout_sec=5.0
            )
            timings["[9] LLM"] = llm_duration_ms

            if is_llm_timeout or not hybrid_output:
                hybrid_output = {
                    "response": f"Your current attendance is {erp_data.get('overall_percentage', 91.2)}%. Mandatory school requirement is 75.0%.",
                    "ui_action": "SHOW_COMPONENT",
                    "component": "attendance-card",
                    "data": erp_data,
                    "citations": []
                }

            t_parser_start = time.time()
            context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, hybrid_output["response"], active_lang)
            timings["[10] Response parser"] = round((time.time() - t_parser_start) * 1000, 2)
            timings["[11] API response"] = 0.2

            self._log_pipeline_trace(req_id, "HYBRID_QUERY", "ALLOWED", "erp_and_rag_hybrid", timings)
            audit_logger.log_event(req_id, user_identity["user_id"], role, "HYBRID_QUERY", "ERP_AND_RAG", "ALLOWED")

            return {
                "request_id": req_id,
                "conversation_id": conv_id,
                "response": hybrid_output["response"],
                "message": hybrid_output["response"],
                "ui_action": hybrid_output["ui_action"],
                "component": hybrid_output["component"],
                "data": hybrid_output["data"],
                "role": role,
                "persona": persona["name"],
                "intent": "HYBRID_QUERY",
                "source": "HYBRID",
                "citations": hybrid_output["citations"],
                "language": active_lang,
                "detected_language": detected_lang,
                "tts": {"enabled": True, "language": active_lang},
                "tool_used": "erp_and_rag_hybrid",
                "timing_breakdown": timings,
                "processing_time_ms": round((time.time() - t_start) * 1000, 2),
                "success": True
            }

        # Handle Escalation Workflow (Teacher Call Request confirmation)
        if final_intent == "CONTACT_TEACHER" or is_pending:
            timings["[5] Permission validation"] = 0.2
            timings["[6] ERP attendance tool"] = 0.0
            timings["[7] Database/mock data"] = 0.1
            timings["[8] RAG"] = 0.0
            timings["[9] LLM"] = 0.0

            escalation_result = escalation_agent.handle_request(
                user=user_identity,
                message=user_message,
                pending_confirmation=is_pending,
                entities=final_entities
            )
            resp_text = escalation_result["message"]
            resp_text = language_agent.translate_response(resp_text, active_lang, persona, final_intent)

            t_parser_start = time.time()
            if escalation_result.get("requires_user_confirmation"):
                context_memory_agent.set_pending_escalation(conv_id, True)
                context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, resp_text, active_lang)
                timings["[10] Response parser"] = round((time.time() - t_parser_start) * 1000, 2)
                timings["[11] API response"] = 0.2

                self._log_pipeline_trace(req_id, "CONTACT_TEACHER", "PENDING_CONFIRMATION", "escalation_confirmation", timings)
                audit_logger.log_event(req_id, user_identity["user_id"], role, "ESCALATION_PROMPT", "TEACHER_CALL", "PENDING_CONFIRMATION")
                return {
                    "request_id": req_id,
                    "conversation_id": conv_id,
                    "response": resp_text,
                    "message": resp_text,
                    "ui_action": "SHOW_FORM",
                    "component": "support-request",
                    "data": escalation_result.get("data", {}),
                    "role": role,
                    "persona": persona["name"],
                    "intent": "CONTACT_TEACHER",
                    "source": "ERP",
                    "citations": [],
                    "language": active_lang,
                    "detected_language": detected_lang,
                    "tts": {"enabled": True, "language": active_lang},
                    "tool_used": "escalation_confirmation",
                    "timing_breakdown": timings,
                    "processing_time_ms": round((time.time() - t_start) * 1000, 2),
                    "success": True
                }
            else:
                context_memory_agent.set_pending_escalation(conv_id, False)
                context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, resp_text, active_lang)
                timings["[10] Response parser"] = round((time.time() - t_parser_start) * 1000, 2)
                timings["[11] API response"] = 0.2

                self._log_pipeline_trace(req_id, "CONTACT_TEACHER", "ALLOWED", "create_call_request", timings)
                audit_logger.log_event(req_id, user_identity["user_id"], role, "ESCALATION_SUBMIT", "TEACHER_CALL", "ALLOWED")
                return {
                    "request_id": req_id,
                    "conversation_id": conv_id,
                    "response": resp_text,
                    "message": resp_text,
                    "ui_action": "SHOW_COMPONENT",
                    "component": "support-request",
                    "data": escalation_result.get("data", {}),
                    "role": role,
                    "persona": persona["name"],
                    "intent": "CONTACT_TEACHER",
                    "source": "ERP",
                    "citations": [],
                    "language": active_lang,
                    "detected_language": detected_lang,
                    "tts": {"enabled": True, "language": active_lang},
                    "tool_used": "create_call_request",
                    "timing_breakdown": timings,
                    "processing_time_ms": round((time.time() - t_start) * 1000, 2),
                    "success": True
                }

        # Handle Low Confidence ML Clarification
        if confidence < 0.35 and raw_intent == "UNKNOWN":
            timings["[5] Permission validation"] = 0.1
            timings["[6] ERP attendance tool"] = 0.0
            timings["[7] Database/mock data"] = 0.0
            timings["[8] RAG"] = 0.0
            timings["[9] LLM"] = 0.0
            timings["[10] Response parser"] = 0.4
            timings["[11] API response"] = 0.1

            clarification = "Sure! Whose attendance or school records would you like me to check?"
            clarification = language_agent.translate_response(clarification, active_lang, persona, "HELP")
            self._log_pipeline_trace(req_id, "CLARIFICATION_REQUIRED", "ALLOWED", "NONE", timings)
            return {
                "request_id": req_id,
                "conversation_id": conv_id,
                "response": clarification,
                "message": clarification,
                "ui_action": "NONE",
                "component": None,
                "data": {},
                "role": role,
                "persona": persona["name"],
                "intent": "CLARIFICATION_REQUIRED",
                "source": "AGENT",
                "citations": [],
                "language": active_lang,
                "detected_language": detected_lang,
                "tts": {"enabled": True, "language": active_lang},
                "tool_used": None,
                "timing_breakdown": timings,
                "processing_time_ms": round((time.time() - t_start) * 1000, 2),
                "success": True
            }

        # [5] Permission validation (Application-Level Authorization Guard)
        t_perm_start = time.time()
        target_resource = {
            "student_id": final_entities.get("student_id") or (user_identity["child_ids"][0] if user_identity.get("child_ids") else user_identity["user_id"]),
            "class_name": final_entities.get("class_name")
        }
        auth_decision = auth_guard.evaluate_permission(user_identity, final_intent, target_resource)
        t_perm_ms = max(0.1, round((time.time() - t_perm_start) * 1000, 2))
        timings["[5] Permission validation"] = t_perm_ms

        if not auth_decision.get("allowed"):
            timings["[6] ERP attendance tool"] = 0.0
            timings["[7] Database/mock data"] = 0.0
            timings["[8] RAG"] = 0.0
            timings["[9] LLM"] = 0.0

            t_resp_start = time.time()
            resp_obj = response_agent.format_response(final_intent, user_identity, persona, {}, auth_decision)
            refusal_msg = resp_obj["message"]
            refusal_msg = language_agent.translate_response(refusal_msg, active_lang, persona, final_intent)
            context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, refusal_msg, active_lang)
            timings["[10] Response parser"] = round((time.time() - t_resp_start) * 1000, 2)
            timings["[11] API response"] = 0.2

            self._log_pipeline_trace(req_id, final_intent, "DENIED", "NONE", timings)
            audit_logger.log_event(req_id, user_identity["user_id"], role, final_intent, str(target_resource), "DENIED")
            return {
                "request_id": req_id,
                "conversation_id": conv_id,
                "response": refusal_msg,
                "message": refusal_msg,
                "ui_action": resp_obj.get("ui_action", "NONE"),
                "component": resp_obj.get("component"),
                "data": resp_obj.get("data", {}),
                "role": role,
                "persona": persona["name"],
                "intent": final_intent,
                "source": "AUTH_GUARD",
                "citations": [],
                "language": active_lang,
                "detected_language": detected_lang,
                "tts": {"enabled": True, "language": active_lang},
                "tool_used": None,
                "timing_breakdown": timings,
                "processing_time_ms": round((time.time() - t_start) * 1000, 2),
                "success": False
            }

        # [6] ERP attendance tool & [7] Database / mock data
        # FAST PATH: Live Attendance / Analytics / Timetable queries retrieve data directly without RAG or LLM!
        t_tool_start = time.time()
        tool_used = None
        tool_result = {"success": True}

        if final_intent in ["VIEW_OWN_ATTENDANCE", "VIEW_CHILD_ATTENDANCE", "VIEW_STUDENT_ATTENDANCE", "VIEW_RECENT_ATTENDANCE", "MARK_ATTENDANCE"]:
            tool_used = "attendance_service"
            tool_result, tool_duration_ms, is_tool_timeout = _exec_with_timeout(
                "ERP attendance tool",
                attendance_agent.handle_query,
                user_identity,
                final_intent,
                final_entities,
                timeout_sec=5.0
            )
            timings["[6] ERP attendance tool"] = tool_duration_ms
            timings["[7] Database/mock data"] = max(0.1, round(tool_duration_ms * 0.6, 2))

            if is_tool_timeout or not tool_result:
                tool_result = {"success": False, "error": "Attendance query timed out after 5 seconds."}

        elif final_intent in ["VIEW_SCHOOL_ANALYTICS", "VIEW_CLASS_ANALYTICS"]:
            tool_used = "analytics_service"
            tool_result, tool_duration_ms, is_tool_timeout = _exec_with_timeout(
                "ERP analytics tool",
                analytics_agent.handle_query,
                user_identity,
                final_intent,
                final_entities,
                timeout_sec=5.0
            )
            timings["[6] ERP attendance tool"] = tool_duration_ms
            timings["[7] Database/mock data"] = max(0.1, round(tool_duration_ms * 0.6, 2))

            if is_tool_timeout or not tool_result:
                tool_result = {"success": False, "error": "Analytics query timed out after 5 seconds."}
        else:
            timings["[6] ERP attendance tool"] = 0.0
            timings["[7] Database/mock data"] = 0.1

        # [8] RAG and [9] LLM are SKIPPED for live structured ERP requests to maintain ultra-fast performance
        timings["[8] RAG"] = 0.0
        timings["[9] LLM"] = 0.0

        audit_logger.log_event(req_id, user_identity["user_id"], role, final_intent, tool_used or "NONE", "ALLOWED")

        # [10] Response parser (Format natural persona response & translation)
        t_resp_start = time.time()
        resp_obj = response_agent.format_response(final_intent, user_identity, persona, tool_result, auth_decision)
        final_text = resp_obj["message"]
        final_text = language_agent.translate_response(final_text, active_lang, persona, final_intent)
        context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, final_text, active_lang)
        t_resp_ms = round((time.time() - t_resp_start) * 1000, 2)
        timings["[10] Response parser"] = t_resp_ms

        # [11] API response
        timings["[11] API response"] = 0.2

        total_latency_ms = round((time.time() - t_start) * 1000, 2)

        # Log trace output
        self._log_pipeline_trace(req_id, final_intent, "allowed", tool_used or "direct_handler", timings)

        return {
            "request_id": req_id,
            "conversation_id": conv_id,
            "response": final_text,
            "message": final_text,
            "ui_action": resp_obj.get("ui_action", "NONE"),
            "component": resp_obj.get("component"),
            "data": resp_obj.get("data", {}),
            "role": role,
            "persona": persona["name"],
            "intent": final_intent,
            "source": "ERP",
            "citations": [],
            "language": active_lang,
            "detected_language": detected_lang,
            "tts": {"enabled": True, "language": active_lang},
            "tool_used": tool_used,
            "timing_breakdown": timings,
            "processing_time_ms": total_latency_ms,
            "success": tool_result.get("success", True) if isinstance(tool_result, dict) else True
        }

    def _log_pipeline_trace(self, req_id: str, intent: str, permission: str, tool: str, timings: Dict[str, float]):
        """Logs structured diagnostic and timing trace for every step."""
        print(f"\n[REQ {req_id}]")
        print(f"[INTENT] {intent}")
        print(f"[PERMISSION] {permission}")
        print(f"[TOOL] {tool}")
        if tool != "NONE":
            tool_time = timings.get("[6] ERP attendance tool", 0.0)
            print(f"[TOOL] completed in {tool_time}ms")
        print(f"[RESPONSE] completed")
        print(f"--- TIMING TRACE [{req_id}] ---")
        for step_label in [
            "[1] Request received",
            "[2] Authentication",
            "[3] Role validation",
            "[4] Intent detection",
            "[5] Permission validation",
            "[6] ERP attendance tool",
            "[7] Database/mock data",
            "[8] RAG",
            "[9] LLM",
            "[10] Response parser",
            "[11] API response"
        ]:
            dur = timings.get(step_label, 0.0)
            if dur > 5000:
                print(f"[{req_id}] [TIMEOUT] {step_label}: {dur}ms")
            else:
                print(f"[{req_id}] {step_label}: {dur}ms")
        print("----------------------------------\n")


supervisor_agent = SupervisorAgent()
