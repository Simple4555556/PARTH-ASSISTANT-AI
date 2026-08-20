"""
PARTH ASSISTANT AI — Structured Security Audit Logger
Records sensitive operational events without exposing secret credentials or tokens.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Configure file & stream logger
logging.basicConfig(level=logging.INFO)
audit_logger_instance = logging.getLogger("PARTH_AUDIT_LOG")


class AuditLogger:
    SENSITIVE_KEYS = {"password", "password_hash", "token", "access_token", "jwt", "api_key", "secret"}

    def _sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = {}
        for k, v in data.items():
            if k.lower() in self.SENSITIVE_KEYS:
                sanitized[k] = "[REDACTED_SECRET]"
            elif isinstance(v, dict):
                sanitized[k] = self._sanitize(v)
            else:
                sanitized[k] = v
        return sanitized

    def log_event(
        self,
        request_id: str,
        user_id: str,
        role: str,
        action: str,
        resource: str,
        result: str,
        extra_details: Optional[Dict[str, Any]] = None
    ):
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": request_id,
            "user_id": user_id,
            "role": role,
            "action": action,
            "resource": resource,
            "result": result
        }

        if extra_details:
            event["details"] = self._sanitize(extra_details)

        audit_logger_instance.info(json.dumps(event))
        return event


audit_logger = AuditLogger()
