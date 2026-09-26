# FYP Progress Report
## Project: AI Mental Health Chatbot (MindCare AI)
**Date:** August 27, 2026
**Status:** In Progress

---

## Project Overview

MindCare AI is an AI-powered mental health support chatbot that combines natural language processing, emotion analysis, and knowledge-based response generation to provide accessible mental health support. The system supports English, Roman Urdu, and Urdu script.

---

## 1. FRONTEND — ✅ COMPLETED

The complete frontend is built using **Streamlit** and is fully functional.

### 1.1 Public Pages (No Login Required)

| Page | File | Status |
|---|---|---|
| Landing / Marketing Page | `ui/landing.py` | ✅ Done |
| About Page | `ui_pages/about.py` | ✅ Done |
| Exercises Page | `ui/exercises.py` | ✅ Done |
| Demo Chat (public trial) | `ui/demo_chat.py` | ✅ Done |
| Games Page | `ui/games.py` | ✅ Done |
| Auth Page (Login / Signup / Forgot Password) | `ui/auth.py` | ✅ Done |
| Sticky Navigation Bar | `components/navbar.py` | ✅ Done |

### 1.2 Authenticated Pages (After Login)

| Page | File | Status |
|---|---|---|
| Dashboard | `ui/dashboard.py` | ✅ Done |
| AI Chat | `ui/chat.py` | ✅ Done |
| Mood Analytics | `ui/mood.py` | ✅ Done |
| Journal | `ui/journal.py` | ✅ Done |
| Games (Calm Colors) | `ui/games.py` | ✅ Done |
| Chat History | `ui/history.py` | ✅ Done |
| Sidebar Navigation | `ui/sidebar.py` | ✅ Done |
| Admin Panel | `ui_pages/admin.py` | ✅ Done |

### 1.3 Auth System

- Email + Password login
- OTP email verification for new accounts
- Forgot password with 6-digit reset code
- Session-based authentication

### 1.4 Multilingual Support (Frontend)

- English input → English response
- Roman Urdu input → Roman Urdu response
- Urdu Unicode script → Urdu script response
- Language detected automatically in Python (no LLM guessing)

### 1.5 Frontend Design

- Purple gradient professional theme throughout
- Fully responsive layout
- Sticky navbar for public pages
- Animated sidebar for logged-in users
- Custom CSS design system (`layout_utils.py`)

---

## 2. BACKEND — 🔄 IN PROGRESS

Backend is built using **FastAPI** and runs locally.

### 2.1 AI Models — ✅ TRAINED & INTEGRATED

All models are fine-tuned DistilRoBERTa transformers, saved locally.

| Model | Folder | Task | Status |
|---|---|---|---|
| Emotion Detection | `models/emotion_dair_ai_roberta` | 28-class emotion classification | ✅ Done |
| Stress Detection | `models/stress_roberta` | Binary (Stress / No Stress) | ✅ Done |
| Depression Detection | `models/depression_v2` | Binary (Depression / No Depression) | ✅ Done |
| GoEmotions RoBERTa | `models/goemotions_roberta` | Multi-label emotion | ✅ Done |
| Reddit Mental Health | `models/reddit_mental_health` | Mental health topic classification | ✅ Done |

### 2.2 RAG Pipeline — ✅ DONE

| Component | File | Status |
|---|---|---|
| Document Loader (PDFs + URLs) | `app/ai/rag/loader.py` | ✅ Done |
| Text Chunking | `app/ai/rag/pipeline.py` | ✅ Done |
| Embeddings (all-MiniLM-L6-v2) | `app/ai/rag/embeddings.py` | ✅ Done |
| FAISS Vector Store | `app/ai/rag/vector_store.py` | ✅ Done |
| Retriever | `app/ai/rag/retriever.py` | ✅ Done |
| CounselChat Dataset → RAG | `app/ai/counsel_chat/` | ✅ Done |

**Knowledge Base sources:**
- CBT Model Worksheet (PDF)
- DSM-5 (PDF)
- Psychotherapy references (PDF)
- WHO Depression fact sheet (Web)
- CounselChat dataset (therapist Q&A pairs)

### 2.3 LLM Integration — ✅ DONE

| Component | File | Status |
|---|---|---|
| LLM Factory (ChatOllama / llama3.2:1b) | `app/ai/llm/llm.py` | ✅ Done |
| Multilingual Prompt Templates | `app/ai/llm/prompt.py` | ✅ Done |
| Language Detection (Python-side) | `app/ai/llm/prompt.py` | ✅ Done |

### 2.4 Integrated Chat Pipeline — ✅ DONE

The `/chat` endpoint runs this full pipeline per request:

```
User message
    → Language detection (Python)
    → Emotion detection model
    → Stress detection model
    → Depression detection model
    → FAISS retriever (top-4 chunks)
    → Language-specific LLM prompt
    → LLM generates response
    → Returns: response + emotion + stress + depression + confidence scores
```

### 2.5 API Endpoints — ✅ DONE

| Endpoint | Method | Description | Status |
|---|---|---|---|
| `/` | GET | Health check | ✅ Done |
| `/chat` | POST | Full AI chat pipeline | ✅ Done |
| `/predict` | POST | Emotion + stress + depression analysis | ✅ Done |
| `/auth/*` | POST | Auth routes (defined) | 🔄 Not registered |
| `/journal/*` | POST | Journal routes (defined) | 🔄 Not registered |
| `/mood/*` | POST | Mood routes (defined) | 🔄 Not registered |
| `/voice/*` | POST | Voice routes (defined) | 🔄 Not registered |

### 2.6 Datasets Used for Training

| Dataset | Folder | Used For |
|---|---|---|
| Emotion Dataset | `datasets/emotion_dataset` | Emotion model training |
| CounselChat | `datasets/counsel_chat` | RAG knowledge base |
| Depression Dataset v1 & v2 | `datasets/depression`, `datasets/depression_v2` | Depression model training |
| Stress Dataset | `datasets/stress` | Stress model training |
| GoEmotions Multilabel | `datasets/goemotions_multilabel` | Emotion model training |
| Reddit Mental Health | Scraped | Mental health classification |

### 2.7 Additional Backend Modules (Defined, Pending Full Integration)

| Module | File | Status |
|---|---|---|
| Redis Session Management | `app/redis/session.py` | 🔄 Implemented, not connected |
| Redis Rate Limiting | `app/redis/rate_limit.py` | 🔄 Implemented, not connected |
| Redis Cache | `app/redis/cache.py` | 🔄 Implemented, not connected |
| Database Models (SQLAlchemy) | `app/database/models.py` | 🔄 Defined, not wired |
| Auth Service | `app/services/auth_service.py` | 🔄 Defined, not wired |
| Journal Service | `app/services/journal_service.py` | 🔄 Defined, not wired |
| Mood Service | `app/services/mood_service.py` | 🔄 Defined, not wired |
| Voice (STT/TTS/Whisper) | `app/voice/` | 🔄 Defined, not wired |
| RAG+LLM Evaluation | `app/ai/evaluation_rag_llm/` | 🔄 Partial |

---

## 3. OVERALL PROGRESS SUMMARY

| Area | Progress |
|---|---|
| Frontend UI | ✅ 100% Complete |
| AI Models (Training) | ✅ 100% Complete |
| RAG Pipeline | ✅ 100% Complete |
| LLM Integration | ✅ 100% Complete |
| Core Chat API (`/chat`, `/predict`) | ✅ 100% Complete |
| Auth / Journal / Mood / Voice APIs | 🔄 ~40% (defined, needs wiring) |
| Redis / Database Integration | 🔄 ~25% (implemented, not connected) |
| Model Evaluation | 🔄 ~50% |

**Overall FYP Completion Estimate: ~70%**

---

## 4. REMAINING WORK (Backend Focus)

1. **Wire remaining API routes** — register auth, journal, mood, and voice routers in `main.py`
2. **Connect database** — wire SQLAlchemy models to active routes (user data, conversations, mood logs, journal entries)
3. **Redis integration** — enable session management, rate limiting, and response caching
4. **Voice pipeline** — connect Whisper STT and TTS to the `/voice` endpoint
5. **Model evaluation** — complete RAG+LLM evaluation on held-out test sets
6. **Environment config** — wire `.env` variables through `config.py` (currently hardcoded in modules)
7. **Testing** — end-to-end API tests for all routes

---

## 5. TECHNOLOGY STACK

| Layer | Technology |
|---|---|
| Frontend | Python, Streamlit |
| Backend | Python, FastAPI, Uvicorn |
| AI Models | PyTorch, Hugging Face Transformers, DistilRoBERTa |
| LLM | Ollama (llama3.2:1b) via LangChain |
| RAG | LangChain, FAISS, sentence-transformers/all-MiniLM-L6-v2 |
| Database | SQLite / SQLAlchemy |
| Caching | Redis |
| Auth | Email OTP verification |
| Voice | Whisper (STT), TTS |

---

*Report generated: August 27, 2026*
