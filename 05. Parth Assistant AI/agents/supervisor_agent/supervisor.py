"""
Supervisor Agent — Main Orchestrator of Multi-Agent System (Multilingual Response & Security Architecture)
"""

import time
import uuid
from typing import Dict, Any, Optional

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


class SupervisorAgent:
    def __init__(self):
        self.safety_agent = SafetySecurityAgent()

    def process_request(
        self,
        session_user: Dict[str, Any],
        user_message: str,
        conversation_id: Optional[str] = None,
        language_preference: Optional[str] = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        req_id = f"REQ-{uuid.uuid4().hex[:6].upper()}"
        conv_id = conversation_id or f"CONV-{uuid.uuid4().hex[:6].upper()}"

        # 1. Identity & Role extraction from session (NEVER trusts prompt claims)
        user_identity = identity_agent.get_authenticated_identity(session_user)
        role = user_identity["role"]
        persona = persona_agent.get_persona(role)

        # 2. Language Resolution & Memory Priority
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

        # Update Conversation Language Memory
        context_memory_agent.set_language(conv_id, active_lang)

        # 3. Safety & Security Inspection (Prompt Injection / Prompt Extraction)
        safety_check = self.safety_agent.inspect_request(user_message)
        if not safety_check.get("is_safe"):
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
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "success": False
            }

        # 4. ML Intent Detection with Confidence Probabilities
        detected_intent = intent_agent.detect_intent(user_message, user_role=role)
        raw_intent = detected_intent["intent"]
        confidence = detected_intent.get("confidence", 1.0)

        if raw_intent == "FAKE_ROLE_CLAIM":
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
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "success": False
            }

        # 5. Entity Extraction
        extracted_entities = entity_agent.extract_entities(user_message)

        # 6. Context Memory Resolution (multi-turn queries)
        resolved_context = context_memory_agent.resolve_contextual_query(
            conversation_id=conv_id,
            new_intent=raw_intent,
            new_entities=extracted_entities
        )
        final_intent = resolved_context["intent"]
        final_entities = resolved_context["entities"]
        is_pending = resolved_context.get("pending_escalation", False)

        # ── RAG ROUTING: Pure School Policy & Knowledge Queries ────────────
        if final_intent == "KNOWLEDGE_QUERY":
            rag_output = rag_agent.handle_query(
                question=user_message,
                user_identity=user_identity,
                language=active_lang,
                persona=persona
            )
            audit_logger.log_event(req_id, user_identity["user_id"], role, "KNOWLEDGE_QUERY", "RAG_VECTORSTORE", "ALLOWED")
            context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, rag_output["response"], active_lang)
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
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "success": rag_output["success"]
            }

        # ── HYBRID ROUTING: Synthesizing Live ERP Records + RAG Policy ──────
        if final_intent == "HYBRID_QUERY":
            # 1. Fetch live ERP attendance data
            erp_intent = "VIEW_CHILD_ATTENDANCE" if role == "PARENT" else "VIEW_OWN_ATTENDANCE"
            erp_res = attendance_agent.handle_query(user_identity, erp_intent, final_entities)
            erp_data = erp_res.get("data", {})

            # 2. Retrieve official attendance policy via RAG
            rag_res = rag_service.query("What is the minimum mandatory attendance requirement for students?", user_role=role)

            # 3. Synthesize hybrid answer via LLM
            hybrid_output = llm_service.generate_hybrid_response(
                question=user_message,
                erp_data=erp_data,
                rag_result=rag_res,
                language=active_lang,
                persona=persona
            )
            audit_logger.log_event(req_id, user_identity["user_id"], role, "HYBRID_QUERY", "ERP_AND_RAG", "ALLOWED")
            context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, hybrid_output["response"], active_lang)
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
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "success": True
            }

        # Handle Escalation Workflow (Teacher Call Request confirmation)
        if final_intent == "CONTACT_TEACHER" or is_pending:
            escalation_result = escalation_agent.handle_request(
                user=user_identity,
                message=user_message,
                pending_confirmation=is_pending,
                entities=final_entities
            )
            resp_text = escalation_result["message"]
            resp_text = language_agent.translate_response(resp_text, active_lang, persona, final_intent)

            if escalation_result.get("requires_user_confirmation"):
                context_memory_agent.set_pending_escalation(conv_id, True)
                context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, resp_text, active_lang)
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
                    "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                    "success": True
                }
            else:
                context_memory_agent.set_pending_escalation(conv_id, False)
                context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, resp_text, active_lang)
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
                    "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                    "success": True
                }

        # Handle Low Confidence ML Clarification
        if confidence < 0.35 and raw_intent == "UNKNOWN":
            clarification = "Sure! Whose attendance or school records would you like me to check?"
            clarification = language_agent.translate_response(clarification, active_lang, persona, "HELP")
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
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "success": True
            }

        # 7. Application-Level Authorization Guard
        target_resource = {
            "student_id": final_entities.get("student_id") or (user_identity["child_ids"][0] if user_identity["child_ids"] else user_identity["user_id"]),
            "class_name": final_entities.get("class_name")
        }
        auth_decision = auth_guard.evaluate_permission(user_identity, final_intent, target_resource)

        if not auth_decision.get("allowed"):
            audit_logger.log_event(req_id, user_identity["user_id"], role, final_intent, str(target_resource), "DENIED")
            resp_obj = response_agent.format_response(final_intent, user_identity, persona, {}, auth_decision)
            refusal_msg = resp_obj["message"]
            refusal_msg = language_agent.translate_response(refusal_msg, active_lang, persona, final_intent)

            context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, refusal_msg, active_lang)
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
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "success": False
            }

        # 8. Route to Specialized ERP Agent & Tool Layer
        t_api_start = time.time()
        tool_used = None
        tool_result = {"success": True}

        if final_intent in ["VIEW_OWN_ATTENDANCE", "VIEW_CHILD_ATTENDANCE", "VIEW_RECENT_ATTENDANCE", "MARK_ATTENDANCE"]:
            tool_used = "attendance_tools"
            tool_result = attendance_agent.handle_query(user_identity, final_intent, final_entities)
        elif final_intent in ["VIEW_SCHOOL_ANALYTICS", "VIEW_CLASS_ANALYTICS"]:
            tool_used = "analytics_tools"
            tool_result = analytics_agent.handle_query(user_identity, final_intent, final_entities)

        api_latency_ms = round((time.time() - t_api_start) * 1000, 2)
        audit_logger.log_event(req_id, user_identity["user_id"], role, final_intent, tool_used or "NONE", "ALLOWED")

        # 9. Format Natural Persona Response in Selected Language
        resp_obj = response_agent.format_response(final_intent, user_identity, persona, tool_result, auth_decision)
        final_text = resp_obj["message"]
        final_text = language_agent.translate_response(final_text, active_lang, persona, final_intent)

        # Update Conversation Memory
        context_memory_agent.update_context(conv_id, final_intent, final_entities, user_message, final_text, active_lang)

        total_latency_ms = round((time.time() - start_time) * 1000, 2)

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
            "processing_time_ms": total_latency_ms,
            "success": tool_result.get("success", True)
        }


supervisor_agent = SupervisorAgent()

