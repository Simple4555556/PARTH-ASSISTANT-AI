# PARTH ASSISTANT AI — SECURITY ARCHITECTURE & AUDIT REPORT

## 1. Executive Summary

PARTH ASSISTANT AI enforces a **zero-trust, multi-layered security architecture**. Security and data isolation are never entrusted to prompt engineering or LLM outputs alone; they are strictly enforced in deterministic backend middleware, JWT authentication guards, and tool-level authorization checks.

---

## 2. Role-Based Access Control (RBAC) Matrix

| Operation / Resource | STUDENT | PARENT | TEACHER | PRINCIPAL | Enforcement Mechanism |
|---|---|---|---|---|---|
| **Own Attendance & Records** | ✅ ALLOWED | ✅ (Linked Child Only) | ✅ ALLOWED | ✅ ALLOWED | `AuthorizationMiddleware` + `db.get_student` |
| **Other Student Records (IDOR)** | ❌ **DENIED (403)** | ❌ **DENIED (403)** | ✅ (Academic View) | ✅ ALLOWED | Server-side user_id & child_ids check |
| **Mark Student Attendance** | ❌ **DENIED (403)** | ❌ **DENIED (403)** | ✅ (Assigned Classes) | ✅ ALLOWED | `require_role([TEACHER, PRINCIPAL])` |
| **School-Wide Analytics** | ❌ **DENIED (403)** | ❌ **DENIED (403)** | ❌ **DENIED** | ✅ ALLOWED | `require_role([PRINCIPAL])` |
| **Raw / Full Database Access** | ❌ **DENIED (403)** | ❌ **DENIED (403)** | ✅ (Academic Database) | ✅ (School Database) | Intent guard + Role evaluation |
| **Escalation / Teacher Call Request** | ❌ DENIED | ✅ ALLOWED | ❌ N/A | ✅ ALLOWED | `require_role([PARENT, PRINCIPAL])` |
| **Public Account Registration** | ✅ ALLOWED | ✅ ALLOWED | ✅ (Requires Code) | ❌ **FORBIDDEN (403)** | Explicit endpoint restriction |

---

## 3. Core Security Pillars

### A. Authentication & Password Security
- **Bcrypt Hashing**: All passwords are encrypted using `bcrypt` (12 salt rounds). Plaintext passwords are never stored in databases or logs.
- **JWT Access Tokens**: Encoded with HS256 algorithm and explicit expiration (`exp`), subject ID (`sub`), and role claims (`role`).
- **Session Revocation (Logout)**: Tokens are invalidated via backend blacklist on `/api/auth/logout`.
- **Public Principal Registration Prohibition**: Principal accounts cannot be self-registered via public endpoints (`POST /api/auth/register/principal` strictly returns `HTTP 403 Forbidden`).

### B. Data Isolation & IDOR Protection
- **Student Data Isolation**: Students are strictly bounded to their own `user_id`. Queries for other students (`student_id=S102` when logged in as `S101`) are blocked at both the API and Tool levels.
- **Parent Child-Data Isolation**: Parents can only access records of their linked children (`child_ids`). Attempts to query unlinked students return `HTTP 403 Forbidden`.
- **Teacher Class Boundaries**: Teachers can only mark attendance for students within their assigned grades/classes (`assigned_classes`).

### C. AI Brain & Tool-Level Authorization
- **Deterministic Permission Guard**: `SupervisorAgent` delegates authorization to `AuthorizationMiddleware` before calling any ERP tools.
- **Independent Tool-Layer Defense**: Every ERP tool (`attendance_tools`, `student_tools`, `analytics_tools`) internally verifies the caller's authenticated identity and resource ownership.

### D. Prompt Injection & Jailbreak Defense
- **Safety Inspection Agent**: Scans input for prompt extraction (`"system prompt"`, `"developer instructions"`), credential extraction (`"api key"`, `"secret"`), and role spoofing (`"I am the principal"`).
- **Immutable Identity**: Authenticated roles are read exclusively from cryptographically verified JWT tokens, NEVER from chat messages.

### E. Multilingual Security
- Language switching (across all 11 supported languages: English, Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Punjabi, Kannada, Malayalam, Urdu) never alters or bypasses user permissions.

### F. Audit Logging & Credential Redaction
- `AuditLogger` automatically redacts sensitive keys (`password`, `password_hash`, `token`, `jwt`, `api_key`, `secret`) from all operational logs.

---

## 4. Vulnerability Disclosure & Reporting

For security inquiries or reporting potential vulnerabilities, please contact the Parth Assistant AI Security Team at `security@parth-assistant.edu`.
