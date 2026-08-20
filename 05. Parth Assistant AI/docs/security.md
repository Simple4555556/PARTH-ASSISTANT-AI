# Security Architecture Documentation — PARTH ASSISTANT AI

## Security Pipeline Overview

```
User Request
   │
   ▼
[JWT Session Authentication] ──► Extracts user_id & role from token (Never trusts prompt claims)
   │
   ▼
[Rate Limiting Middleware] ──► Checks 30 req/min threshold (Returns HTTP 429 if exceeded)
   │
   ▼
[Safety & Security Guard] ──► Inspects prompt injection / system prompt extraction keywords
   │
   ▼
[Centralized RBAC Matrix] ──► Evaluates user role permissions (STUDENT, PARENT, TEACHER, PRINCIPAL)
   │
   ▼
[Resource-Level Guard] ──► Validates student_id ownership, parent child links, teacher assigned classes
   │
   ▼
[Tool-Level Validation] ──► Re-validates arguments & user scope before Mock ERP tool calls
   │
   ▼
[Sanitized Audit Logging] ──► Records event without passwords, JWTs, or secret keys
```

---

## Permission Matrix Summary

| Role | Allowed Actions | Resource Scope | Denied Actions |
| :--- | :--- | :--- | :--- |
| **STUDENT** | View own attendance, subject logs | Self (`user_id == target_student_id`) | View other students, Mark attendance, Analytics |
| **PARENT** | View child attendance, Request teacher call | Linked children (`child_id in parent.child_ids`) | Unrelated students, Mark attendance, Analytics |
| **TEACHER** | View & mark class attendance | Assigned classes (`10-A`, `9-B`) | Unassigned classes, Principal analytics |
| **PRINCIPAL** | School analytics, class reports | All school records | N/A |

---

## Defensive Measures

1. **Prompt Injection Defense**: Keyword filtering blocks instructions attempting to override system behavior.
2. **System Prompt Protection**: Returns safe natural refusal ("I can help with school information available to your account, but I can't provide restricted information or internal system instructions.").
3. **Role Claim Hardening**: Natural language claims (e.g. "I am the principal") do not override authenticated JWT session role.
4. **Sanitized Audit Logger**: Events recorded to log output strip passwords, tokens, and API key fields (`[REDACTED_SECRET]`).
