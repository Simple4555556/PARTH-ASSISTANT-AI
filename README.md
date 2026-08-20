# PARTH ASSISTANT AI — Human-Like AI School Assistant

> **Competition-Grade Applied AI System for School ERP Ecosystem**

![PARTH ASSISTANT AI](https://img.shields.io/badge/Status-Production_Ready-brightgreen)
![Python](https://img.shields.io/badge/Backend-FastAPI_Python_3.11-blue)
![React](https://img.shields.io/badge/Frontend-React_Vite_Vanilla_CSS-cyan)
![Security](https://img.shields.io/badge/Security-Centralized_RBAC_Resource_Guards-red)
![ML](https://img.shields.io/badge/ML-TF--IDF_Logistic_Regression_97.47%25-green)
![Multilingual](https://img.shields.io/badge/Multilingual-11_Languages_%2B_Hinglish-purple)
![Tests](https://img.shields.io/badge/Tests-108%2F108_Passing-brightgreen)

---

## Executive Summary

**PARTH ASSISTANT AI** is a production-style, human-like AI School Assistant integrated with a School ERP Ecosystem. Unlike standard chatbots, Parth Assistant AI functions as a secure, role-aware, context-aware, multimodal AI interface that respects deterministic application-level authorization and tool-level resource validation.

It caters to 4 primary user roles:
1. **Student** — Academic Assistant
2. **Parent** — Parent Support Assistant
3. **Teacher** — Teaching Assistant
4. **Principal / Management** — Executive Management Assistant

---

## Clean Project Structure

```
PARTH-ASSISTANT-AI/
│
├── 01. Student/
│   └── student-portal/
│
├── 02. Parent/
│   └── parent-portal/
│
├── 03. Management/
│   └── management-portal/
│
├── 04. Staff/
│   └── staff-portal/
│
└── 05. Parth Assistant AI/
    └── xyz-ai/
        ├── frontend/              # React (Vite) Conversational-First UI + AIAvatar
        ├── backend/               # FastAPI Server, Bcrypt Auth & JWT Engine
        ├── agents/                # 12 Specialized Agent Modules
        │   ├── supervisor_agent/
        │   ├── identity_role_agent/
        │   ├── intent_agent/
        │   ├── entity_agent/
        │   ├── context_memory_agent/
        │   ├── persona_agent/
        │   ├── attendance_agent/
        │   ├── analytics_agent/
        │   ├── escalation_agent/
        │   ├── language_agent/
        │   ├── safety_security_agent/
        │   └── response_agent/
        ├── tools/                 # Validated ERP Execution Tools
        ├── mock_services/         # Decoupled Mock ERP Services
        ├── database/              # Persistence Engine & Seed Records
        ├── ml/                    # ML Intent Classifier (TF-IDF + Logistic Regression)
        ├── voice/                 # STT Normalization & Multilingual TTS Synthesis
        ├── avatar/                # Visual AI Avatar State Specifications
        ├── tests/                 # 108 Automated Tests (100% Passing)
        ├── docs/                  # Architecture & Security Documentation
        ├── .env.example           # Environment Configuration Template
        ├── requirements.txt       # Python Dependencies
        ├── SECURITY.md            # Zero-Trust Security Policy & Matrix
        └── README.md              # Master System Documentation
```


---

## System Architecture

```
             PARTH ASSISTANT AI
                     │
       ┌─────────────┴─────────────┐
       │                           │
     CHAT                       SECURITY
       │                           │
       ▼                           ▼
   Supervisor                  RBAC (permissions.py)
       │                    Authorization (auth_middleware.py)
       ▼                    Prompt Defense (safety_security.py)
 Intent + Entity             Audit Logs (audit_logger.py)
       │
       ▼
  ML (predict.py - 97.47% Accuracy)
       │
       ▼
  Context Memory (context_memory.py)
       │
       ▼
   ERP Tools (tools/)
       │
       ▼
   Real Mock Data (db_engine.py - 20 Students, 8 Parents, 8 Teachers)
       │
       ▼
 Multilingual Response (language.py - 11 Indian Languages + Hinglish)
```

### Execution Flow Pipeline

```
User Request
   │
   ▼
[JWT Session Authentication] ──► Extracts user_id & role from token (Never trusts prompt claims)
   │
   ▼
[Rate Limiter Middleware] ──► Enforces 30 req/min limit (Returns HTTP 429 when exceeded)
   │
   ▼
[Safety & Security Guard] ──► Inspects prompt injection / system prompt extraction attacks
   │
   ▼
[ML Intent Classifier] ──► TF-IDF + Logistic Regression Intent Prediction (97.47% Accuracy)
   │
   ▼
[Entity & Context Memory] ──► Multi-turn query resolution ("What about last month?")
   │
   ▼
[Centralized Authorization Guard] ──► Evaluates RBAC & Resource Ownership boundaries
   │
   ▼
[Tool Execution Layer] ──► Executes validated Mock ERP Tool calls
   │
   ▼
[Response & Language Agent] ──► Formats persona response in selected Indian Language / Hinglish
```

---

## Machine Learning Performance Metrics

- **Model Type**: TF-IDF Vectorizer (1-gram & 2-gram) + Logistic Regression
- **Training Dataset**: 79 labeled queries across 12 intents
- **Accuracy**: **97.47%**
- **F1 Score**: **0.9736**
- **Precision**: **0.9768**
- **Recall**: **0.9747**

*Metrics report saved in [`ml/metrics/evaluation_report.json`](file:///e:/Parth%20Assistent/05.%20Parth%20Assistant%20AI%20Repository/xyz-ai/ml/metrics/evaluation_report.json).*

---

## Multilingual Support (11 Indian Languages + Hinglish)

Supported languages:
English (`en`), Hindi (`hi`), Tamil (`ta`), Telugu (`te`), Marathi (`mr`), Bengali (`bn`), Gujarati (`gu`), Punjabi (`pa`), Kannada (`kn`), Malayalam (`ml`), Urdu (`ur`). Supports mixed Hinglish queries naturally.

---

## Quick Start & Local Setup

### 1. Backend Setup

```bash
cd "05. Parth Assistant AI Repository/xyz-ai"

# Install dependencies
pip install -r requirements.txt

# Train ML Intent Classifier
python ml/train.py

# Evaluate ML Model Metrics
python ml/evaluate.py

# Run Automated Test Suite (149/149 passing)
python -m pytest tests

# Launch FastAPI Backend Server
python -m uvicorn backend.main:app --reload --port 8000
```

Backend API Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd "05. Parth Assistant AI Repository/xyz-ai/frontend"

npm install
npm run dev
```

Frontend App: `http://localhost:5173`

---

## Phase Progress Summary

- [x] **Phase 1**: Core architecture, 4 dashboards, mock data, JWT auth, AI drawer shell
- [x] **Phase 2**: AI Brain, 12 specialized agents, ERP tools layer, mock APIs, escalation workflow
- [x] **Phase 3**: Centralized RBAC permissions, resource guards, rate limiter, audit logger, ML Intent classifier (97.47% accuracy), 11 Indian languages + Hinglish support, UI language selector, 34 passing tests
- [x] **Phase 4**: Voice (STT/TTS), AI avatar lip-sync, bcrypt auth, token revocation, registration endpoints, security audit, GitHub-safe secrets management, 108 passing tests
- [x] **Phase 5**: LLM Engine, RAG Pipeline, MemoryVectorStore, Grounded Response Synthesis, Hybrid RAG+ERP queries, Role-Based Retrieval Access Control, Anti-Hallucination, Citations, Multilingual RAG (11 languages), PolicyCard UI component, 149 passing tests

---

## Architecture: RAG + ERP + Hybrid

```
USER
 │
Chat / Voice / Avatar
 │
Language Agent
 │
Supervisor
 │
Intent Agent
 │
 ├── KNOWLEDGE_QUERY ─────► RAG Agent ─► VectorStore ─► LLM ─► PolicyCard + Citations
 │                                           ▲
 │                                   Role-Based Filtering
 │
 ├── ERP QUERY ──────────► Permission ─► ERP Tool ─► AttendanceCard / TimetableCard
 │
 └── HYBRID_QUERY ────────► ERP + RAG ─► LLM Synthesis ─► Combined Answer + Citations
```

| Layer | Technology |
|---|---|
| Embedding Model | TF-IDF Char N-Gram (multilingual, no API key needed) |
| Vector Store | MemoryVectorStore (swappable via BaseVectorStore) |
| LLM Engine | Hybrid Local Engine (Gemini/OpenAI via `LLM_PROVIDER` env) |
| Document Format | Markdown with structured metadata headers |
| Role Filtering | Pre-retrieval RBAC (before context reaches LLM) |
| Hallucination Control | Strict grounding — no answer if context not found |
| Citations | Title + Source + Section (no internal vector IDs exposed) |
