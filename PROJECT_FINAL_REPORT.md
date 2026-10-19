# MindCare AI — Project Final Report
**Comprehensive Technical Architecture, Methodology, Tooling, and System Audit**

**Project Title:** MindCare AI — Multilingual AI-Powered Mental Health Support System  
**Academic Degree:** Bachelor of Science in Computer Science / Software Engineering / AI (Final Year Project)  
**Date:** October 2026  
**Document Classification:** Final Project Technical Master Report  

---

## Table of Contents

1. [Executive Summary & System Architecture](#1-executive-summary--system-architecture)
2. [Complete Technology & Tooling Inventory (Deep-Dive)](#2-complete-technology--tooling-inventory-deep-dive)
   - [2.1 Backend Framework & API Infrastructure](#21-backend-framework--api-infrastructure)
   - [2.2 Frontend Framework & Web UI](#22-frontend-framework--web-ui)
   - [2.3 Deep Learning & Transformer Inference](#23-deep-learning--transformer-inference)
   - [2.4 Machine Learning & Scientific Computing](#24-machine-learning--scientific-computing)
   - [2.5 Retrieval-Augmented Generation (RAG) & Vector Search](#25-retrieval-augmented-generation-rag--vector-search)
   - [2.6 Large Language Model (LLM) & Local Runtime](#26-large-language-model-llm--local-runtime)
   - [2.7 Relational Database & Connection Pooling](#27-relational-database--connection-pooling)
   - [2.8 Cryptography, Authentication & Security](#28-cryptography-authentication--security)
   - [2.9 Audio, Voice & Speech Processing](#29-audio-voice--speech-processing)
   - [2.10 Visualization & Charting Engines](#210-visualization--charting-engines)
   - [2.11 Natural Language Processing Utilities](#211-natural-language-processing-utilities)
3. [Database Architecture & Connection Pool Mechanics](#3-database-architecture--connection-pool-mechanics)
4. [AI/ML Pipeline & Transformer Classifiers (Deep-Dive)](#4-aiml-pipeline--transformer-classifiers-deep-dive)
5. [RAG Pipeline — Clinical Grounding & Vector Search](#5-rag-pipeline--clinical-grounding--vector-search)
6. [LLM Dialogue Engine, Multilingual Routing & Quality Guardrails](#6-llm-dialogue-engine-multilingual-routing--quality-guardrails)
7. [Clinical Safety & Privacy Guardrails](#7-clinical-safety--privacy-guardrails)
8. [Frontend Features & User Experience](#8-frontend-features--user-experience)
9. [Identified Weaknesses, Gaps & Outstanding Issues](#9-identified-weaknesses-gaps--outstanding-issues)
10. [Academic Defense Strategy & Base Papers](#10-academic-defense-strategy--base-papers)
11. [Conclusion & Future Roadmap](#11-conclusion--future-roadmap)

---

## 1. Executive Summary & System Architecture

### 1.1 The Clinical Problem & Motivation
Mental health conditions affect approximately 1 in 4 individuals globally. In Pakistan, the psychiatric treatment gap is acute: with fewer than **500 licensed psychiatrists serving a population exceeding 240 million**, there is less than one psychiatrist per 500,000 citizens. Furthermore, prohibitive private therapy fees, systemic societal stigma, geographic concentration of clinicians in major urban hubs, and the total lack of conversational health tools supporting local dialects (specifically Roman Urdu and Urdu Unicode) prevent millions from receiving early psychosocial support.

### 1.2 The MindCare AI Solution
**MindCare AI** is an intelligent, privacy-preserving, multilingual mental health support platform. Unlike generic LLM chatbots that hallucinate unverified medical advice or operate exclusively in English, MindCare AI establishes an integrated multi-tier architecture:
1. **Real-time Diagnostic Screening**: Three fine-tuned Transformer models run in parallel on every user utterance to classify emotion (6 classes), stress (binary), and depression indicators (binary).
2. **Evidence-Based Grounding (RAG)**: A FAISS vector database retrieves validated clinical literature from DSM-5 diagnostic criteria, WHO intervention manuals, Cognitive Behavioral Therapy (CBT) worksheets, and 4,567 licensed therapist dialogue records from CounselChat.
3. **Multilingual Local LLM Dialogue**: An on-premise Large Language Model (`llama3.2:3b` executed via Ollama) delivers empathetic, conversational support in English, Roman Urdu (Latin script), and Urdu Unicode (Arabic script) with 0ms cloud dependency and complete patient data sovereignty.
4. **Deterministic Clinical Guardrails**: An instant, non-generative interceptor bypasses AI inference for crisis/suicidal ideation to route users directly to verified Pakistani helplines (Umang `0311-7786264`, Govt `1166`), while an automated language validation loop eliminates Hindi loanword contamination from Roman Urdu responses.

### 1.3 High-Level System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   CLIENT LAYER (Browser)                                │
│                     http://localhost:8501 (Desktop, Mobile, Tablet)                     │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │ HTTP / WebSockets
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND TIER (Streamlit 1.54.0)                           │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │ UI Modules: Landing | Auth | Chat (Voice+Text) | Mood | Journal | Games | Admin   │  │
│  │ State: st.session_state (user_session, JWT token, navigation, chat history)       │  │
│  │ API Adapter: frontend/db.py -> frontend/api_client.py (REST requests with Bearer) │  │
│  └──────────────────────────────────────────┬────────────────────────────────────────┘  │
└─────────────────────────────────────────────┼───────────────────────────────────────────┘
                                              │ REST API (JSON / HTTP Bearer)
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND TIER (FastAPI on Port 8000)                        │
│                                                                                         │
│  ┌───────────────────────┬───────────────────────┬───────────────────────────────────┐  │
│  │      Auth Router      │      Mood Router      │          Journal Router           │  │
│  │   /auth/login, /reg   │   POST /mood, GET     │       POST /journal, GET          │  │
│  ├───────────────────────┼───────────────────────┼───────────────────────────────────┤  │
│  │   App Data Router     │     Admin Router      │            Chat Router            │  │
│  │ /conversations, /hist │  /admin/users, /logs  │     POST /predict, POST /chat     │  │
│  └───────────────────────┴───────────────────────┴─────────────────┬─────────────────┘  │
│                                                                    │                    │
│                        REQUEST LIFECYCLE (POST /chat)              │                    │
│                                                                    ▼                    │
│                 ┌───────────────────────────────────────────────────────┐               │
│                 │ 1. Emergency Crisis Guardrail (Regex / Keyword Check) │               │
│                 │    ├── [CRISIS] -> Bypass LLM -> Return Helplines     │               │
│                 │    └── [SAFE]   -> Proceed to Step 2                  │               │
│                 │ 2. Privacy Redaction (Mask CNIC, Phone, Email)        │               │
│                 │ 3. Deterministic Language Detection (Urdu/Roman/Eng)  │               │
│                 │ 4. Parallel Classifiers (DistilBERT/RoBERTa/DeBERTa)  │               │
│                 │ 5. FAISS Vector Retrieval (Top-4 Clinical Chunks)     │               │
│                 │ 6. Sliding Window History Assembly (Last 3 Turns)     │               │
│                 │ 7. Prompt Assembly -> Ollama LLM (llama3.2:3b)        │               │
│                 │ 8. Roman Urdu Validation Parser (Filter Hindi Words)  │               │
│                 └───────────────────────────────────────────────────────┘               │
└─────────────────────────────────┬──────────────────────────────────────┬────────────────┘
                                  │                                      │
              SQL via psycopg2    │                                      │ Local In-Memory
              Threaded Pool       ▼                                      ▼ PyTorch & FAISS
┌──────────────────────────────────────────────┐       ┌──────────────────────────────────┐
│              DATA STORAGE TIER               │       │         LOCAL AI ASSETS          │
│                                              │       │                                  │
│  PostgreSQL 15 (fyp_chatbot)                 │       │  1. Emotion Model (DistilBERT)   │
│  - users (id, email, password_hash, admin)   │       │  2. Depression Model (RoBERTa)   │
│  - conversations (id, user_id, title)        │       │  3. Stress Model (DeBERTa-v3)    │
│  - messages (id, conv_id, role, content)     │       │  4. FAISS Index (MiniLM-L6-v2)   │
│  - mood (id, user_id, mood, created_at)      │       │  5. Ollama Daemon (llama3.2:3b)  │
│  - journal (id, user_id, entry, created_at)  │       │                                  │
│  - user_activity (id, user_id, action, time) │       │                                  │
│  - password_reset_tokens (token, code, exp)  │       │                                  │
└──────────────────────────────────────────────┘       └──────────────────────────────────┘
```

---

## 2. Complete Technology & Tooling Inventory (Deep-Dive)

This section provides an exhaustive accounting of every single tool, library, and framework deployed across MindCare AI, detailing:
1. **Exact Library & Version**
2. **Role & Architectural Purpose**
3. **How It Is Implemented in Code**
4. **How It Operates Internally (Under the Hood)**

---

### 2.1 Backend Framework & API Infrastructure

#### `FastAPI` (Version: Latest / 0.115+)
- **Purpose**: Serves as the central asynchronous REST API engine. Coordinates all incoming HTTP requests from the Streamlit frontend, enforces payload schemas, handles dependency injection, and routes requests to the AI services.
- **How It Is Used**: Defined in `backend/app/main.py`. Mounts modular APIRouters (`chat_router`, `auth_router`, `mood_router`, `journal_router`, `application_router`). Implements modern lifespan context management (`lifespan(_app: FastAPI)`) to initialize and tear down database connection pools cleanly.
- **How It Works Under the Hood**: Built on top of Starlette (for high-performance ASGI web routing) and Pydantic (for data validation). Leverages Python type hints to serialize/deserialize JSON payloads, performs automatic OpenAPI/Swagger documentation generation at `/docs`, and runs concurrently across an asynchronous event loop.

#### `Uvicorn`
- **Purpose**: High-performance Asynchronous Server Gateway Interface (ASGI) web server that executes the FastAPI application.
- **How It Is Used**: Runs the backend server using `uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`.
- **How It Works Under the Hood**: Built on `uvloop` (an ultra-fast Cython wrapper around `libuv`, the C library powering Node.js) and `httptools` (a Python binding for the NodeJS HTTP parser). Handles TCP connection establishment, SSL/TLS termination, HTTP parsing, and feeds requests into the FastAPI ASGI pipeline.

#### `Pydantic` (Version: 2.12.5) & `pydantic_core`
- **Purpose**: Data parsing, strict type validation, and settings management for API requests and responses.
- **How It Is Used**: Implemented in `backend/app/database/schemas.py`. Defines request/response models: `PredictionRequest`, `PredictionResponse`, `ChatMessage`, `ChatRequest`, `ChatResponse`, `RegisterRequest`, `LoginRequest`, `MoodCreate`, `JournalCreate`, and `ActivityCreate`.
- **How It Works Under the Hood**: Pydantic v2 is completely rewritten in Rust (`pydantic-core`). When an HTTP JSON body arrives, Pydantic converts and validates types against class annotations at compiled Rust speeds. If validation fails, it generates standardized HTTP 422 Unprocessable Entity errors before application logic executes.

#### `python-dotenv` (Version: 1.2.2)
- **Purpose**: Twelve-factor application configuration; loads environment variables from `.env` files into `os.environ`.
- **How It Is Used**: Called in `backend/app/core/config.py` via `load_dotenv(BACKEND_DIR / ".env", override=False)` to inject database credentials, JWT secrets, SMTP keys, and pool limits.
- **How It Works Under the Hood**: Parses key-value pairs from text files, strips comments and whitespace, and populates Python's `os.environ` mapping without overriding preexisting system-level variables unless explicitly directed.

#### `requests` (Version: 2.32.5)
- **Purpose**: Synchronous HTTP client library used for service-to-service communication and frontend-to-backend communication.
- **How It Is Used**: Implemented in `frontend/api_client.py` and `frontend/db.py` to transmit REST requests (`GET`, `POST`, `DELETE`) with attached JWT Bearer tokens to the FastAPI backend at `http://127.0.0.1:8000`.
- **How It Works Under the Hood**: Built upon `urllib3`. Manages persistent HTTP keep-alive connection pooling, handles connection retry logic, and parses response byte streams into native Python dictionaries via `.json()`.

---

### 2.2 Frontend Framework & Web UI

#### `Streamlit` (Version: 1.54.0)
- **Purpose**: The reactive web application framework powering the entire MindCare AI user interface.
- **How It Is Used**: Declared in `frontend/app.py`. Manages multi-page routing (`Landing`, `Auth`, `Dashboard`, `Chat`, `Mood Analytics`, `Journal`, `Exercises`, `Games`, `Chat History`, `Admin Panel`). Maintains session state across browser interactions using `st.session_state`.
- **How It Works Under the Hood**: Operates a stateful execution model. Every time a user interacts with a widget (click, keystroke, dropdown change), Streamlit re-executes the Python script from top to bottom. It establishes a bi-directional WebSocket connection between the Python backend process and the React/Tornado frontend engine, diffing the generated component trees and pushing incremental Virtual DOM updates.

#### `streamlit.components.v1`
- **Purpose**: Allows custom HTML, CSS, and raw JavaScript injection into the Streamlit DOM.
- **How It Is Used**: Deployed in `frontend/app.py` to inject parent-window DOM scripts:
  1. `installNavigationScrollReset`: Resets scroll position to `(0, 0)` upon page switching.
  2. `styleToggle`: Injects persistent CSS into the parent iframe document so the sidebar expand/collapse button (`[data-testid="stSidebarCollapseButton"]` / `[data-testid="stExpandSidebarButton"]`) remains visible and styled.
- **How It Works Under the Hood**: Embeds an isolated `<iframe>` within the Streamlit page that can manipulate parent window elements (when operating in the same origin) via `window.parent.document`.

#### `streamlit-mic-recorder` (Version: 0.0.8)
- **Purpose**: Browser-based audio recording widget for speech input.
- **How It Is Used**: Integrated in `frontend/ui/chat.py` to capture user voice recordings directly from their microphone.
- **How It Works Under the Hood**: Uses the browser's HTML5 `MediaStream Recording API` via WebRTC. Captures microphone PCM audio buffers in the client's browser, encodes them into a WebM/Opus byte array, and sends the raw bytes across the WebSocket back to Streamlit's Python runtime.

#### `Watchdog` (Version: 6.0.0)
- **Purpose**: File system monitoring tool for developer hot-reloading.
- **How It Is Used**: Automatically observes changes in `frontend/` and `backend/` Python files during development, triggering immediate browser reruns.
- **How It Works Under the Hood**: Hooks into Windows OS kernel-level file system notification APIs (`ReadDirectoryChangesW`) to receive instant non-polling file modification events.

---

### 2.3 Deep Learning & Transformer Inference

#### `PyTorch` (`torch`, `torchvision`, `torchaudio`)
- **Purpose**: The core deep learning tensor computation and neural network execution framework.
- **How It Is Used**: Executes forward-pass inference for all fine-tuned Transformer models in:
  - `backend/app/ai/emotion_detection/predict.py`
  - `backend/app/ai/depression_detection/predict.py`
  - `backend/app/ai/stress_detection/predict.py`
  - `backend/evaluation/reddit_mental_health/evaluate_reddit_model.py`
- **How It Works Under the Hood**: Provides an N-dimensional `Tensor` object with GPU/CPU acceleration. When `model.eval()` and `torch.no_grad()` are invoked, PyTorch disables autograd computational graph construction, drastically reducing memory overhead and executing optimized C++ CPU tensor kernels (AVX2/AVX-512) for matrix multiplications.

#### `Hugging Face Transformers` (Version: 4.55.4)
- **Purpose**: State-of-the-art Natural Language Understanding (NLU) model repository and inference abstraction.
- **How It Is Used**: Loads pretrained architectures via `AutoTokenizer.from_pretrained()` and `AutoModelForSequenceClassification.from_pretrained()` for:
  1. `distilbert-base-uncased` (Emotion Model)
  2. `roberta-base` (Depression Model)
  3. `microsoft/deberta-v3-base` (Stress Model)
  4. `roberta-base` (Reddit Mental Health Model)
- **How It Works Under the Hood**: Implements modular Transformer blocks: multi-head self-attention, feedforward projection layers, layer normalization, and classification heads (`Linear(hidden_size, num_labels)`). Handles input token ID mapping, attention masking, positional encoding, and logits generation.

#### `Accelerate` (Version: 1.9.0)
- **Purpose**: Optimized model training and device placement framework.
- **How It Is Used**: Leveraged during model fine-tuning in Google Colab notebooks (`MindCare_AI_DAIR_AI_Emotion_3_Model_Complete_Colab.ipynb`) to manage mixed-precision (FP16) training across NVIDIA T4/A100 GPUs without manual CUDA boilerplate.
- **How It Works Under the Hood**: Automatically manages hardware accelerators, handles gradient accumulation, and wraps PyTorch data loaders with optimal pin-memory and non-blocking CUDA stream operations.

#### `Safetensors` (Version: 0.7.0)
- **Purpose**: Fast, safe storage and loading of neural network weights.
- **How It Is Used**: Serializes and deserializes model weights in `backend/models/`.
- **How It Works Under the Hood**: Developed by Hugging Face in Rust. Unlike Python's standard `pickle` format (which is vulnerable to arbitrary remote code execution), `safetensors` contains only raw tensor buffers and a JSON metadata header. It utilizes zero-copy memory mapping (`mmap`), allowing models to load into RAM almost instantaneously.

#### `Tokenizers` & `SentencePiece`
- **Purpose**: High-speed tokenization engines converting raw strings into input IDs and attention masks.
- **How It Is Used**: Tokenizes user text in `predict.py` using Byte-Pair Encoding (BPE for RoBERTa) and WordPiece (for DistilBERT). DeBERTa-v3 utilizes SentencePiece for subword vocabulary segmentation.
- **How It Works Under the Hood**: Implemented in Rust. Tokenizes sentences in microseconds: normalizes Unicode, strips/splits text, applies statistical subword merges, and pads/truncates tensors to `max_length=128`.

---

### 2.4 Machine Learning & Scientific Computing

#### `scikit-learn`
- **Purpose**: Evaluation metrics, train/test dataset splitting, and baseline model comparisons.
- **How It Is Used**: Calculates performance metrics across validation and held-out test splits in evaluation scripts:
  - `accuracy_score`
  - `precision_recall_fscore_support` (Macro-F1, Weighted-F1, Precision, Recall)
  - `confusion_matrix`
- **How It Works Under the Hood**: Efficient C/Cython algorithms that perform statistical matrix evaluation over predicted label vectors versus ground-truth arrays.

#### `NumPy` (Version: 2.2.6)
- **Purpose**: Foundational numerical array operations, mathematical transformations, and probability manipulation.
- **How It Is Used**: Used in prediction post-processing to compute softmax normalization over logits:
  $$\sigma(z)_i = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$
  Extracts prediction probabilities via `np.argmax()` and converts confidence values to native Python percentages.
- **How It Works Under the Hood**: C-based contiguous memory arrays with vectorized SIMD CPU instructions for mathematical operations.

#### `Pandas` (Version: 2.3.3)
- **Purpose**: Structured tabular data manipulation and dataset preparation.
- **How It Is Used**: Ingests and processes training corpora:
  - `CounselChat.csv` (4,567 licensed therapist QA pairs)
  - DAIR-AI emotion CSVs
  - Depression and stress dataset CSVs
  - Experiment evaluation comparison logs (`three_model_comparison.csv`)
- **How It Works Under the Hood**: Manages heterogeneous tabular data structures (DataFrames) backed by NumPy arrays and Apache Arrow, offering vectorized filtering, string cleansing, and missing-value imputation.

---

### 2.5 Retrieval-Augmented Generation (RAG) & Vector Search

#### `FAISS` (`faiss-cpu`)
- **Purpose**: Facebook AI Similarity Search — high-performance vector indexing and dense similarity search engine.
- **How It Is Used**: Stored on disk in `backend/knowledge_base/vector_store/` (`index.faiss` and `index.pkl`). Loaded by `backend/app/ai/rag/vector_store.py` to retrieve the top $k=4$ most clinically relevant document chunks for each incoming user query.
- **How It Works Under the Hood**: Written in highly optimized C++ with OpenMP multi-threading. MindCare AI utilizes FAISS with normalized Euclidean/Inner Product metrics (`IndexFlatIP`). When normalized 384-dimensional query embeddings are searched, inner product computation equals exact Cosine Similarity:
  $$\text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\| \|v\|} = u_{\text{norm}} \cdot v_{\text{norm}}$$
  FAISS scans millions of dimensional vectors in sub-millisecond time.

#### `sentence-transformers` (Version: 5.6.1) — Model: `all-MiniLM-L6-v2`
- **Purpose**: Dense semantic text embedding generation.
- **How It Is Used**: Instantiated in `backend/app/ai/rag/embeddings.py` via:
  ```python
  HuggingFaceEmbeddings(
      model_name="sentence-transformers/all-MiniLM-L6-v2",
      encode_kwargs={"normalize_embeddings": True}
  )
  ```
  Converts both clinical knowledge base chunks and live user questions into dense 384-dimensional semantic vectors.
- **How It Works Under the Hood**: A distilled 6-layer MiniLM model fine-tuned on over 1 billion sentence pairs using a Siamese network architecture (Sentence-BERT). It projects sentences into a continuous vector space where semantically similar thoughts cluster together regardless of lexical overlap.

#### `LangChain` & Sub-packages (`langchain-core`, `langchain-community`, `langchain-huggingface`, `langchain-ollama`)
- **Purpose**: Orchestration framework connecting retrieval stores, prompts, and local LLMs.
- **How It Is Used**:
  - `RecursiveCharacterTextSplitter`: Splits clinical PDFs and CSVs into 500-character chunks with 100-character overlap.
  - `FAISS` LangChain wrapper: Bridges vector retrieval into pipeline chains.
  - `ChatPromptTemplate`: Assembles system instructions, RAG context chunks, classifier cues, and conversational history.
  - `ChatOllama`: Wraps local LLM calls into standard message formats (`SystemMessage`, `HumanMessage`, `AIMessage`).
- **How It Works Under the Hood**: Provides standardized abstract base classes (`Runnable`, `BaseRetriever`, `BaseChatModel`) that compose pipelines via the LangChain Expression Language (LCEL).

#### `PyPDF` & `BeautifulSoup4` (Version: 4.15.0)
- **Purpose**: Clinical document ingestion.
- **How It Is Used**:
  - `PyPDFLoader`: Extracts raw text, chapter titles, and clinical worksheets from DSM-5, CBT worksheets, and WHO stress management manuals.
  - `BeautifulSoup4` (`bs4`): Scrapes and parses the official WHO Depression Fact Sheet HTML into clean markdown text for the vector store.
- **How It Works Under the Hood**: PyPDF traverses the PDF byte tree, extracts font glyphs and content streams, and reconstructs text blocks. BeautifulSoup builds a Document Object Model (DOM) tree from HTML, filtering script tags, styles, and navigational chrome to isolate substantive health guidance.

---

### 2.6 Large Language Model (LLM) & Local Runtime

#### `Ollama` (Local Daemon Runtime)
- **Purpose**: Provides local, zero-cost, private inference for open-weights Large Language Models without third-party cloud API dependencies (OpenAI, Anthropic).
- **How It Is Used**: Runs as a local daemon at `http://localhost:11434`. MindCare AI connects to it via LangChain's `ChatOllama(model="llama3.2:3b", temperature=0.2, num_predict=300)`.
- **How It Works Under the Hood**: Packaged as a Go/C++ service wrapping `llama.cpp`. Quantizes LLM weights (GGUF format, 4-bit/8-bit precision), binds execution to available CPU threads or GPU VRAM, and streams token-by-token generation via an internal REST API.

#### Model: `Llama 3.2:3b` (Meta AI)
- **Purpose**: The conversational generation engine producing warm, empathetic mental health dialogues.
- **How It Is Used**: Generates responses conditioned on the RAG context, user history, and detected mental state.
- **How It Works Under the Hood**: A 3.21-billion parameter autoregressive Transformer decoder with Grouped-Query Attention (GQA) and Rotary Position Embeddings (RoPE). Trained by Meta on over 9 trillion multilingual tokens. Low temperature ($T=0.2$) constrains stochastic sampling, suppressing hallucinations while ensuring strict adherence to clinical guidelines.

---

### 2.7 Relational Database & Connection Pooling

#### `PostgreSQL` (Version: 15 / Port 5432)
- **Purpose**: ACID-compliant persistent relational database for user accounts, chat logs, mood logs, and audit trails.
- **How It Is Used**: Stores tables: `users`, `conversations`, `messages`, `mood`, `journal`, `user_activity`, and `password_reset_tokens`.
- **How It Works Under the Hood**: Multiversion Concurrency Control (MVCC), Write-Ahead Logging (WAL) for fault tolerance, B-tree indexed primary/foreign keys, and relational integrity constraints.

#### `psycopg2-binary` (Version: 2.9.11) & `pool.ThreadedConnectionPool`
- **Purpose**: PostgreSQL driver and thread-safe connection pooling for high-concurrency database transactions.
- **How It Is Used**: Implemented in `backend/app/database/connection.py`. Initializes a pool of minimum 1 and maximum 10 persistent connections (`ThreadedConnectionPool(settings.db_pool_min, settings.db_pool_max, ...)`). Managed via a Python context manager `db_cursor(commit=bool)`.
- **How It Works Under the Hood**: Detailed extensively in [Section 3](#3-database-architecture--connection-pool-mechanics).

---

### 2.8 Cryptography, Authentication & Security

#### `bcrypt`
- **Purpose**: Industry-standard adaptive cryptographic password hashing.
- **How It Is Used**: Implemented in `backend/app/core/security.py`. Hashes new user passwords using `bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))`. Verifies credentials at login via `bcrypt.checkpw()`.
- **How It Works Under the Hood**: An adaptive hash function based on the Blowfish block cipher. Incorporates a 128-bit salt to defeat rainbow-table attacks and an exponential work factor ($2^{12} = 4,096$ iterations), making brute-force hardware cracking computationally infeasible.

#### Legacy `hashlib` SHA-256 Support & Auto-Rehashing
- **Purpose**: Backward-compatibility for legacy user accounts created prior to the 3-tier security refactor.
- **How It Is Used**: `verify_password()` in `security.py` checks if a stored hash starts with `$2` (bcrypt). If not, it compares against `hashlib.sha256()`. If valid, it flags `needs_rehash = True`, prompting `auth_service.py` to transparently upgrade the user's password in PostgreSQL to a salted bcrypt hash upon successful login.
- **How It Works Under the Hood**: Uses `hmac.compare_digest` to prevent timing attacks when comparing hash strings.

#### Stateless JWT Tokens (HMAC-SHA256)
- **Purpose**: Stateless, cryptographically signed API authentication.
- **How It Is Used**: When users log in at `/auth/login`, `create_access_token()` issues a JWT containing `user_id`, `email`, and expiration (`exp`). Frontend attaches this token to HTTP headers as `Authorization: Bearer <token>`. FastAPI dependency `current_claims()` decodes and validates every request.
- **How It Works Under the Hood**: Encodes header and payload as Base64URL strings, signs them with a secret key using HMAC-SHA256, and verifies integrity upon receipt. Expiration is enforced in Python epoch seconds.

#### `smtplib` & Email OTP (Gmail TLS)
- **Purpose**: Transmits 6-digit numeric verification OTP codes for registration and password resets.
- **How It Is Used**: `frontend/ui/email_utils.py` connects to `smtp.gmail.com:587` using TLS encryption.
- **How It Works Under the Hood**: Establishes a TCP socket connection, upgrades the connection via `STARTTLS`, authenticates using an application-specific password, and delivers structured MIME multipart HTML email templates.

---

### 2.9 Audio, Voice & Speech Processing

#### `gTTS` (Google Text-to-Speech / Version: 2.5.4)
- **Purpose**: Synthesizes spoken audio from assistant text responses.
- **How It Is Used**: Used in `frontend/ui/chat.py` to enable audio playback of bot responses.
- **How It Works Under the Hood**: Sends text strings to Google Translate's TTS endpoint, downloads the returned MP3 stream, and serves it through Streamlit's `st.audio()` HTML5 player.

#### `SpeechRecognition` (Version: 3.14.5)
- **Purpose**: Transcribes user voice messages into text.
- **How It Is Used**: Receives audio files recorded by `streamlit_mic_recorder`, processes the WAV audio stream, and transcribes it via `recognizer.recognize_google(audio_data)`.
- **How It Works Under the Hood**: Analyzes audio energy thresholds, frames PCM audio, uploads the payload to Google's speech recognition API, and returns candidate transcript strings.

#### `pydub` (Version: 0.25.1) & `FFmpeg`
- **Purpose**: Audio format conversion.
- **How It Is Used**: Converts browser-recorded WebM/Opus audio buffers into standard 16kHz mono WAV format required by speech recognition engines.
- **How It Works Under the Hood**: `pydub` provides a Python API that invokes the compiled `ffmpeg` binary via subprocess, decoding raw compressed media streams and re-encoding them into uncompressed PCM WAV.

---

### 2.10 Visualization & Charting Engines

#### `Plotly` (`plotly.graph_objects` / Version: 6.5.0)
- **Purpose**: Interactive, dynamic charting for mood analytics and emotional trend tracking.
- **How It Is Used**: Configured in `frontend/ui/mood.py`:
  1. **Mood Trend Timeline**: Spline line charts tracking numeric mood valuations (Angry=1 to Happy=5) over time.
  2. **Mood Distribution Donut**: Hole pie chart displaying emotional log proportions.
  3. **Chat Activity & Stress Correlation**: Dual-axis graph correlating daily user message counts with detected stress indicator frequencies.
- **How It Works Under the Hood**: Generates dynamic JavaScript charts using `plotly.js`, rendering hardware-accelerated interactive SVGs/Canvases in the browser with hover tooltips and zoom controls.

#### `Matplotlib` (Version: 3.10.8) & `Seaborn`
- **Purpose**: Static visualization generation during model evaluation.
- **How It Is Used**: Plots confusion matrices, training loss curves, and validation Macro-F1 trajectories in Google Colab notebooks.
- **How It Works Under the Hood**: Renders raster/vector graphics onto a 2D canvas, computing pixel heatmaps for confusion matrices.

---

### 2.11 Natural Language Processing Utilities

#### `NLTK` (Version: 3.9.3) & `SpaCy`
- **Purpose**: Classical NLP preprocessing, tokenization, stop-word removal, and vocabulary lookups.
- **How It Is Used**: Cleans training texts and evaluates lexical diversity across datasets.

#### `VaderSentiment` & `TextBlob`
- **Purpose**: Baseline sentiment scoring used during early exploratory phases to validate Transformer advantage.

---

## 3. Database Architecture & Connection Pool Mechanics

### 3.1 Relational Schema & Entity Relationships

The relational architecture is deployed on **PostgreSQL 15** (`fyp_chatbot` database) and comprises 7 normalized tables:

```
┌─────────────────────────────────┐           ┌───────────────────────────────────┐
│              users              │           │       password_reset_tokens       │
├─────────────────────────────────┤           ├───────────────────────────────────┤
│ id            : SERIAL PRIMARY  │──┐        │ id         : SERIAL PRIMARY       │
│ username      : VARCHAR(50)     │  │        │ user_id    : INT REFERENCES users │
│ email         : VARCHAR(100) UNQ│  │        │ reset_code : VARCHAR(6)           │
│ password_hash : VARCHAR(255)    │  │        │ token      : VARCHAR(100)         │
│ is_admin      : BOOLEAN         │  │        │ used       : BOOLEAN DEFAULT FALSE│
│ created_at    : TIMESTAMP       │  │        │ expires_at : TIMESTAMP           │
└─────────────────────────────────┘  │        │ created_at : TIMESTAMP           │
                                     │        └───────────────────────────────────┘
          ┌──────────────────────────┼───────────────────────────┐
          │ 1:N                      │ 1:N                       │ 1:N
          ▼                          ▼                           ▼
┌─────────────────────────────────┐  │         ┌─────────────────────────────────┐
│          conversations          │  │         │              mood               │
├─────────────────────────────────┤  │         ├─────────────────────────────────┤
│ id         : SERIAL PRIMARY     │  │         │ id         : SERIAL PRIMARY     │
│ user_id    : INT REFERENCES users  │         │ user_id    : INT REFERENCES users│
│ title      : VARCHAR(255)       │  │         │ mood       : VARCHAR(50)        │
│ created_at : TIMESTAMP         │  │         │ created_at : TIMESTAMP         │
└────────────────┬────────────────┘  │         └─────────────────────────────────┘
                 │ 1:N               │
                 ▼                   │ 1:N     ┌─────────────────────────────────┐
┌─────────────────────────────────┐  │         │             journal             │
│            messages             │  │         ├─────────────────────────────────┤
├─────────────────────────────────┤  │         │ id         : SERIAL PRIMARY     │
│ id              : SERIAL PRIMARY│  │         │ user_id    : INT REFERENCES users│
│ conversation_id : INT (FK)      │  │         │ entry      : TEXT               │
│ user_id         : INT (FK)      │  │         │ created_at : TIMESTAMP         │
│ role            : VARCHAR(20)   │  │         └─────────────────────────────────┘
│ content         : TEXT          │  │
│ created_at      : TIMESTAMP     │  │         ┌─────────────────────────────────┐
└─────────────────────────────────┘  │         │          user_activity          │
                                     │ 1:N     ├─────────────────────────────────┤
                                     └────────▶│ id          : SERIAL PRIMARY    │
                                               │ user_id     : INT REFERENCES users
                                               │ action_type : VARCHAR(50)       │
                                               │ page_name   : VARCHAR(50)       │
                                               │ details     : TEXT              │
                                               │ timestamp   : TIMESTAMP         │
                                               └─────────────────────────────────┘
```

---

### 3.2 Connection Pooling: Why It Matters & How It Works

#### The Engineering Problem Without a Pool
In naive web architectures, every API request initiates a direct database connection:
```
Client -> Request -> Connect to PG (TCP 3-way handshake + TLS + Auth) -> Query -> Close Connection
```
In PostgreSQL, establishing a connection is resource-intensive:
1. The OS performs a network socket handshake.
2. PostgreSQL spawns a dedicated backend process (`postgres: user db [local]`) via `fork()`.
3. Memory structures (work_mem, cache buffers) are allocated.
4. If 50 concurrent requests arrive, 50 processes are forked, exhausting server RAM and spiking latency.

#### MindCare AI's Solution: `ThreadedConnectionPool`
MindCare AI deploys **psycopg2's `ThreadedConnectionPool`** in `backend/app/database/connection.py`:

```python
_pool = pool.ThreadedConnectionPool(
    settings.db_pool_min,  # minconn = 1
    settings.db_pool_max,  # maxconn = 10
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
)
```

#### How the Context Manager Operates
```python
@contextmanager
def db_cursor(commit: bool = False) -> Iterator:
    connection_pool = init_pool()
    connection = connection_pool.getconn()  # 1. Borrow warm connection
    cursor = connection.cursor()
    try:
        yield cursor                        # 2. Execute SQL query
        if commit:
            connection.commit()             # 3. Commit transaction
    except Exception:
        connection.rollback()               # 4. Rollback on failure
        raise
    finally:
        cursor.close()                      # 5. Close cursor
        connection_pool.putconn(connection) # 6. Return connection to pool
```

#### Internal Pool Lifecycle
1. **Startup**: When FastAPI starts, the `lifespan` handler calls `init_pool()`, pre-spawning warm PostgreSQL connections.
2. **Borrowing (`getconn`)**: When a thread requires database access, it retrieves an idle connection instantly from the pool in memory (0ms TCP handshake).
3. **Thread Safety**: `ThreadedConnectionPool` utilizes internal threading mutexes (`threading.Lock()`), ensuring no two worker threads receive the same connection simultaneously.
4. **Transaction Integrity**: If a query encounters an error (e.g., unique email violation), the `except` block intercepts the exception and issues `connection.rollback()`, resetting transaction state before releasing it.
5. **Release (`putconn`)**: The `finally` block guarantees that the connection is never orphaned or leaked, returning it to the pool for reuse.
6. **Graceful Shutdown**: Upon backend server shutdown, the lifespan context executes `close_pool()`, cleanly disconnecting all sockets via `_pool.closeall()`.

---

## 4. AI/ML Pipeline & Transformer Classifiers (Deep-Dive)

### 4.1 The 3-Model Comparative Experiment Protocol

To achieve rigorous academic validation, we refused to arbitrarily select a single model. For each of the three mental health detection challenges, we conducted standardized **3-model comparative experiments** evaluating:
1. **DistilBERT** (`distilbert-base-uncased` - 66.96M parameters)
2. **RoBERTa** (`roberta-base` - 124.65M parameters)
3. **DeBERTa-v3** (`microsoft/deberta-v3-base` - 184.42M parameters)

#### Standardized Experimental Hyperparameters:
- **Learning Rate**: $2 \times 10^{-5}$
- **Epochs**: 3
- **Batch Size**: 16
- **Max Sequence Length**: 128 tokens
- **Optimizer**: AdamW ($\beta_1=0.9, \beta_2=0.999, \epsilon=10^{-8}$)
- **Weight Decay**: 0.01
- **Evaluation Strategy**: Evaluated at the end of each epoch; checkpoint saved based on highest **Validation Macro-F1**.
- **Data Integrity**: **The test set was strictly held out** and never touched during hyperparameter tuning or model selection, ensuring zero data leakage.

---

### 4.2 Benchmark Results Across Tasks

#### Task 1: Emotion Detection (DAIR-AI Dataset, 6 Classes)
*Classes: Sadness, Joy, Love, Anger, Fear, Surprise | Total Samples: 20,000*

| Model Architecture | Parameters | Val Accuracy | Val Macro-F1 | Test Accuracy | Test Macro-F1 | Training Time | Selection Status |
|--------------------|------------|--------------|--------------|---------------|---------------|---------------|------------------|
| **DistilBERT** | **66.96M** | **94.00%** | **0.9136** | **92.60%** | **0.8820** | **5.98 min** | ✅ **SELECTED** |
| DeBERTa-v3 | 184.43M | 94.05% | 0.9130 | 93.55% | 0.8929 | 15.36 min | ❌ Rejected |
| RoBERTa | 124.65M | 93.90% | 0.9118 | 93.00% | 0.8802 | 8.45 min | ❌ Rejected |

*Selection Rationale*: DistilBERT achieved the highest validation Macro-F1 (0.9136). With less than half the parameters of DeBERTa-v3, DistilBERT executes inference in ~12ms on CPU, making it vastly superior for real-time interactive user chats.

---

#### Task 2: Depression Detection (Depression v2 Dataset, Binary)
*Classes: Depression, No Depression | Total Samples: ~5,740*

| Model Architecture | Parameters | Val Accuracy | Val Macro-F1 | Test Accuracy | Test Macro-F1 | Training Time | Selection Status |
|--------------------|------------|--------------|--------------|---------------|---------------|---------------|------------------|
| **RoBERTa** | **124.65M** | **98.26%** | **0.9826** | **98.17%** | **0.9817** | **3.74 min** | ✅ **SELECTED** |
| DeBERTa-v3 | 184.42M | 98.08% | 0.9808 | 97.91% | 0.9791 | 7.43 min | ❌ Rejected |
| DistilBERT | 66.96M | 97.56% | 0.9756 | 98.08% | 0.9808 | 2.31 min | ❌ Rejected |

*Selection Rationale*: RoBERTa achieved the highest validation Macro-F1 (0.9826) and test accuracy (98.17%). Its dynamic masking and extended pretraining enable exceptional discrimination between depressive ideation and standard emotional distress.

---

#### Task 3: Stress Detection (Stress Dataset, Binary)
*Classes: Stress, No Stress | Total Samples: ~3,575*

| Model Architecture | Parameters | Val Accuracy | Val Macro-F1 | Test Accuracy | Test Macro-F1 | Training Time | Selection Status |
|--------------------|------------|--------------|--------------|---------------|---------------|---------------|------------------|
| **DeBERTa-v3** | **184.42M** | **84.45%** | **0.8437** | **81.96%** | **0.8185** | ~14 min | ✅ **SELECTED** |
| RoBERTa | 124.65M | 83.75% | 0.8336 | 78.18% | 0.7758 | ~8 min | ❌ Rejected |
| DistilBERT | 66.96M | 80.57% | 0.8050 | 77.20% | 0.7710 | ~5 min | ❌ Rejected |

*Selection Rationale*: DeBERTa-v3 demonstrated a distinct advantage (+1.01% validation F1 over RoBERTa, +3.87% over DistilBERT). Stress expressions in conversational language are subtle; DeBERTa-v3's disentangled attention mechanism (which decouples word content representations from relative positional distances) successfully captured nuanced contextual strain.

---

#### Task 4: Auxiliary Reddit Mental Health Topic Classifier
*Classes: ADHD, OCD, Aspergers, Depression, PTSD | Total Samples: 625+*

- **Model**: `roberta-base` fine-tuned for multi-class disorder topic extraction.
- **Overall Performance**: Test Accuracy = **85.60%**, Macro-Precision = **89.82%**, Macro-Recall = **85.60%**, Macro-F1 = **85.56%**.
- **Class Breakdown**:
  - OCD: Precision = 100.0%, Recall = 88.0%, F1 = 0.9362
  - Aspergers: Precision = 83.3%, Recall = 100.0%, F1 = 0.9091
  - PTSD: Precision = 100.0%, Recall = 80.0%, F1 = 0.8889
  - Depression: Precision = 65.8%, Recall = 100.0%, F1 = 0.7937
  - ADHD: Precision = 100.0%, Recall = 60.0%, F1 = 0.7500

---

### 4.3 Runtime Inference Execution & Parallelization

When a user submits a message, executing three Transformer models sequentially would add 100–250ms of overhead. MindCare AI runs all three classifiers concurrently in `backend/app/services/rag_chat_service.py` using Python's `ThreadPoolExecutor`:

```python
def run_detectors(text: str) -> Tuple[dict, dict, dict]:
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_emotion    = executor.submit(predict_emotion, text)
        f_stress     = executor.submit(predict_stress, text)
        f_depression = executor.submit(predict_depression, text)
        return f_emotion.result(), f_stress.result(), f_depression.result()
```

Each prediction function executes the following inner logic:
1. **Tokenization**: Formats text into tensors with truncation (`max_length=128`) and attention masks.
2. **Forward Pass**: Passes tensor through the model inside a `torch.no_grad()` block.
3. **Softmax & Argmax**:
   ```python
   logits = outputs.logits
   probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]
   predicted_index = int(np.argmax(probabilities))
   confidence = float(probabilities[predicted_index] * 100)
   ```
4. **Confidence Thresholding**: Labels scoring below `LOW_CONF = 60.0%` are automatically flagged with `(low confidence — treat as unreliable)` when injected into the LLM prompt.

---

## 5. RAG Pipeline — Clinical Grounding & Vector Search

### 5.1 The Role of RAG in Clinical AI
Generative Large Language Models suffer from stochastic hallucination. In mental healthcare, a hallucinated coping mechanism or an invented psychiatric definition is potentially dangerous. MindCare AI employs Retrieval-Augmented Generation (RAG) to enforce **non-parametric grounding**: the LLM is strictly constrained to synthesize guidance derived from verified clinical literature.

### 5.2 Curated Clinical Knowledge Base

| Source Document | Modality / Format | Size / Depth | Clinical Purpose |
|-----------------|-------------------|--------------|------------------|
| **CounselChat** | CSV dataset | 4,567 QA rows | Authentic, licensed human therapist responses to real patient concerns. |
| **DSM-5** | PDF document | Comprehensive criteria | Evidence-based diagnostic criteria for major depressive disorder, generalized anxiety, PTSD, and mood disorders. |
| **CBT Model Worksheet** | PDF (SimplePractice) | Structured exercises | Cognitive Behavioral Therapy worksheets (thought reframing, cognitive distortions). |
| **Techniques of Psychotherapy** | PDF manual | Clinical compendium | Psychoeducation, grounding techniques, exposure pacing, and supportive therapy modalities. |
| **Doing What Matters in Times of Stress** | PDF (World Health Org) | Illustrated coping guide | Evidence-based stress coping mechanisms developed by WHO for global populations. |
| **WHO Depression Fact Sheet** | Web URL (Scraped) | Official fact sheet | Epidemiological facts, evidence-based treatments, and global lifestyle recommendations. |

---

### 5.3 Ingestion, Chunking & Embedding Math

```
[Raw Clinical Documents]
          │
          ▼
RecursiveCharacterTextSplitter (chunk_size=500, chunk_overlap=100)
          │
          ▼
sentence-transformers/all-MiniLM-L6-v2 (384-dimensional vector)
          │
          ▼
L2 Normalization: v_norm = v / ||v||_2
          │
          ▼
FAISS IndexFlatIP (Inner Product Search on Normalized Vectors = Cosine Similarity)
```

1. **Chunk Size Optimization**: Chunks are set to 500 characters with 100-character overlap. A 500-character chunk corresponds to roughly 75–100 words (the exact length of an individual CBT intervention or therapist advice snippet), ensuring high semantic density without diluting retrieval similarity.
2. **Vector Normalization**: By setting `normalize_embeddings=True`, every document vector and query vector is normalized to unit Euclidean length ($\|v\|_2 = 1$).
3. **Retrieval**: When a user asks a question, FAISS computes the cosine similarity across all indexed chunks in memory and returns the top $k=4$ most similar text segments.

---

## 6. LLM Dialogue Engine, Multilingual Routing & Quality Guardrails

### 6.1 Deterministic Language Detection (Zero-LLM Overhead)

Prompting an LLM to identify the incoming language introduces latency and frequent errors on informal dialects. MindCare AI implements deterministic Python-side language routing in `backend/app/ai/llm/prompt.py`:

```python
_URDU_SCRIPT_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")

def detect_language(text: str) -> str:
    if _URDU_SCRIPT_RE.search(text):
        return "urdu"
    words = re.findall(r"[a-zA-Z]+", text.lower())
    hits = sum(1 for w in words if w in _ROMAN_URDU_WORDS) # 65+ Pakistani anchor words
    ratio = hits / len(words) if words else 0
    if hits >= 2 and ratio >= 0.25:
        return "roman_urdu"
    return "english"
```

---

### 6.2 4-Step Therapeutic Prompt Architecture

Every user message is structured through an evidence-based 4-step therapeutic dialogue flow:
1. **Acknowledge**: Specifically name and reflect the user's emotion without robotic repetition (*"That sounds really overwhelming, and it makes complete sense why you feel that way."*).
2. **Validate & Normalize**: Reassure the user that their emotional reaction is a natural human response, reducing internalized shame or self-blame.
3. **Practical Support**: Seamlessly integrate **one** actionable CBT technique (e.g., 4-4-4 box breathing, 5-4-3-2-1 sensory grounding, cognitive reframing) without clinical jargon or bulleted lists.
4. **Invite Conversation**: Conclude with a warm, open-ended question that encourages further sharing (*"What has been weighing on you the most today?"*).

---

### 6.3 Roman Urdu Quality Guardrails & Auto-Regeneration Loop

Commercial LLMs commonly suffer from **Hindi/Sanskrit contamination** when prompted in Roman Urdu, generating words like *samasya*, *chikitsa*, *anand*, or *parivaar* that are linguistically alien to Pakistani Urdu speakers.

MindCare AI implements a post-generation validation parser (`backend/app/ai/llm/validator.py`):
1. **Forbidden Word Lexicon**: Scans against 50+ formal Hindi/Sanskrit loanwords.
2. **Script Purity Check**: Ensures no Arabic/Urdu Unicode characters bleed into Roman Urdu mode.
3. **English Leakage Check**: Ensures the model does not abandon Roman Urdu to reply in English.
4. **Auto-Regeneration Loop**: If validation fails, `build_correction_prompt()` dynamically creates a reprimand prompt explaining the exact violation and forces the LLM to rewrite the response. This retry loop runs up to `MAX_REGENERATE_ATTEMPTS = 2`.

---

## 7. Clinical Safety & Privacy Guardrails

### 7.1 Emergency Crisis Interceptor

Safety is paramount in mental health AI. If a user exhibits active suicidal ideation or self-harm intent, **the LLM is completely bypassed**. Machine learning models must never be allowed to generate unstructured text during acute life-threatening crises.

```
User Prompt: "I just want to end my life, I can't do this anymore"
       │
       ▼
detect_crisis(question)  ──► Matches high-severity suicidal intent keywords
       │
       ▼
[BYPASS ALL LLM / RAG / CLASSIFIER INFERENCE]
       │
       ▼
Immediate Return of Verified Emergency Helplines (0ms Generation Latency)
```

#### Verified Regional Emergency Resources Provided:
- **Pakistan**:
  - Umang Mental Health Helpline: `0311-7786264`
  - Rozan Helpline: `0800-22444`
  - Government Mental Health Helpline: `1166`
  - National Emergency Services: `1122` (Rescue) / `15` (Police)
- **International**:
  - US/Canada Suicide & Crisis Lifeline: `988`
  - Crisis Text Line: Text `HOME` to `741741`
  - UK Emergency: `111` / `999`

---

### 7.2 Automated Privacy Redaction (Data Sanitization)

Before any text is stored in PostgreSQL or forwarded to internal logs, sensitive personal identifiers are scrubbed via `backend/app/services/privacy.py`:
- **Pakistani CNIC Numbers**: `\b\d{5}[-\s]?\d{7}[-\s]?\d\b` $\rightarrow$ `[CNIC REDACTED]`
- **Pakistani Mobile Numbers**: `(?:\+?92|0)\s?(?:3\d{2})[-\s]?\d{3}[-\s]?\d{4}` $\rightarrow$ `[PHONE REDACTED]`
- **Email Addresses**: Standard RFC regex $\rightarrow$ `[EMAIL REDACTED]`

---

## 8. Frontend Features & User Experience

The frontend is built using **Streamlit 1.54.0** with custom CSS styling and component-level JavaScript bridges:

1. **AI Chat Interface (`frontend/ui/chat.py`)**:
   - **Typewriter Effect**: Streams character-by-character generation for a comforting, human-like cadence.
   - **AI Diagnostic Signal Chips**: Displays model outputs transparently:
     `Emotion: Sadness · 92%` | `Stress: Elevated · 81%` | `Wellness: Concerning · 98%`
     accompanied by a clinical disclaimer: *"These AI signals are not a medical diagnosis."*
   - **Voice Input & Output**: Seamless microphone recording and text-to-speech audio playback.
   - **Multi-Turn Context Sliding Window**: Retains the last 3 conversation exchanges (`ChatMessage`) in session memory, maintaining conversational continuity.
2. **Interactive Mood Analytics (`frontend/ui/mood.py`)**:
   - Quick mood logging with single-click emoji selectors (Happy, Neutral, Sad, Anxious, Angry).
   - Dynamic Plotly trend graphs, distribution donut charts, and statistical mood variety counts.
   - Cross-correlation analysis linking chat keyword frequencies with logged emotional states.
3. **Reflective Journaling (`frontend/ui/journal.py`)**:
   - Encrypted personal reflection diary with automatic timestamping and mood tagging.
   - Serialized with schema versioning (`JOURNAL_V1:` JSON payload).
4. **8 Guided CBT & Mindfulness Exercises (`frontend/ui/exercises.py`)**:
   - Quick Relief: 1-Minute Reset, Pause and Orient.
   - Breathwork: Box Breathing (4-4-4-4), 4-7-8 Relaxing Breath.
   - Mindfulness: Gentle Body Scan, Mindful Moment.
   - Grounding: 5-4-3-2-1 Sensory Grounding, Steady Object Focus.
5. **CalmColors Mindfulness Game (`frontend/ui/games.py`)**:
   - A sequential cognitive memory game designed to pull users out of anxiety-induced panic cycles through visual and attentional grounding.
6. **Admin Audit Dashboard (`frontend/ui_pages/admin.py`)**:
   - User account tracking, conversation message audits, and activity access logs.

---

## 9. Identified Weaknesses, Gaps & Outstanding Issues

During our rigorous end-to-end audit of the codebase, the following technical and architectural items were identified:

### 9.1 Solved During Audit
- **Git Merge Conflict in Prompt Templates (RESOLVED)**:  
  *Finding*: In `backend/app/ai/llm/prompt.py`, git merge conflict markers (`<<<<<<< Updated upstream`, `=======`, `>>>>>>> Stashed changes`) were present inside triple-quoted strings across `_ENGLISH_SYSTEM`, `_ROMAN_URDU_SYSTEM`, and `_URDU_SYSTEM`.  
  *Impact*: While not crashing the Python parser, these markers were literally injected into the LLM system prompt.  
  *Resolution*: Successfully cleaned and resolved in this audit session; prompt templates now contain clean, unified guidelines and examples.

---

### 9.2 Technical & Machine Learning Limitations
1. **Stress Classifier Test Accuracy (81.96%)**:  
   While DeBERTa-v3 outperformed RoBERTa and DistilBERT, its 81.96% accuracy is lower than Depression (98.17%) and Emotion (92.60%). Stress language in text frequently overlaps with ordinary academic or workplace vocabulary, leading to occasional false positives.
2. **Context Window Ceiling of Local 3B LLM**:  
   Operating `llama3.2:3b` on local CPU/consumer GPU limits the practical context budget to 1,800 tokens. In extensive conversations exceeding 5–6 exchanges, earlier conversational history must be truncated by the sliding window manager to avoid out-of-memory errors.
3. **Single Modality (Text-Centric Inference)**:  
   Although audio input is transcribed via SpeechRecognition, the emotion/stress classifiers analyze only the resulting text transcript, ignoring acoustic vocal biomarkers (prosody, pitch jitter, speech rate) that provide strong clinical indicators of distress.

---

### 9.3 Architectural & Security Limitations
1. **Keyword-Based Crisis Filter Edge Cases**:  
   The crisis guardrail operates primarily via regex and keyword matching. Complex or metaphorical suicidal expressions that avoid explicit trigger words (*"I want to sleep and never wake up"*) might bypass the hard-stop interceptor and enter the generative LLM pipeline.
2. **API Rate Limiting & DoS Protection**:  
   The FastAPI backend currently lacks IP-based rate limiting (e.g., via `slowapi` or Redis token-bucket middleware). In a public cloud deployment, excessive concurrent requests could degrade local Ollama inference performance.
3. **Automated Continuous Integration (CI) Test Suite**:  
   While individual components have evaluation scripts, the repository lacks an automated end-to-end `pytest` suite validating API endpoints, DB transactions, and token expiration in an automated CI/CD pipeline.

---

## 10. Academic Defense Strategy & Base Papers

For an academic thesis defense before a faculty examination panel, MindCare AI is grounded in three seminal peer-reviewed research papers:

```
                              ┌────────────────────────────────────────┐
                              │        ACADEMIC BASE PAPERS            │
                              └───────────────────┬────────────────────┘
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 ▼                                ▼                                ▼
       ╔═══════════════════╗            ╔═══════════════════╗            ╔═══════════════════╗
       ║  MAIN BASE PAPER  ║            ║ SUPPORTING PAPER 1║            ║ SUPPORTING PAPER 2║
       ║  RoBERTa (2019)   ║            ║    RAG (2020)     ║            ║   S-BERT (2019)   ║
       ║   Liu et al.      ║            ║   Lewis et al.    ║            ║ Reimers & Gurevych║
       ╚═══════════════════╝            ╚═══════════════════╝            ╚═══════════════════╝
         Primary Classifier               Clinical Knowledge               Dense Embedding
         Backbone Architecture            Retrieval Grounding              Vector Similarity
```

---

### 10.1 Main Base Paper
> **"RoBERTa: A Robustly Optimized BERT Pretraining Approach"**  
> *Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, Veselin Stoyanov (Facebook AI / University of Washington)*  
> **Citation**: arXiv:1907.11692, 2019. [https://arxiv.org/abs/1907.11692](https://arxiv.org/abs/1907.11692)

- **Role in Project**: Serves as the backbone architecture for our Depression Classifier (98.26% validation F1) and Reddit Mental Health Classifier (85.60% accuracy), and the primary benchmark competitor across all 3-model evaluations.
- **Panel Defense Q&A**:
  - *Panel Question*: "Why did you choose RoBERTa instead of the original BERT architecture?"
  - *Defense Response*: "Liu et al. (2019) proved that BERT was significantly undertrained. RoBERTa optimizes BERT by removing the Next Sentence Prediction (NSP) objective—which was shown to degrade downstream classification performance—and introducing dynamic masking across larger minibatches with 10× more pretraining data. In our experiments, RoBERTa achieved a 98.26% validation F1 score on depression classification, validating that its robust pretraining translates directly to superior clinical text discrimination."
  - *Panel Question*: "If RoBERTa is your main base paper, why is your production Emotion model DistilBERT?"
  - *Defense Response*: "This demonstrates our empirical research integrity. We did not dogmatically deploy RoBERTa for every task; we conducted rigorous 3-model comparative evaluations. For emotion detection, DistilBERT achieved a higher validation Macro-F1 (0.9136 vs 0.9118) while utilizing less than half the parameters (66.96M vs 124.65M) and executing inference 40% faster, making it the mathematically superior engineering choice for real-time mobile/web chat."

---

### 10.2 Supporting Base Paper 1
> **"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"**  
> *Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela (Facebook AI Research / UCL / NYU)*  
> **Citation**: NeurIPS 2020. [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

- **Role in Project**: Provides the theoretical and architectural foundation for our clinical RAG pipeline (FAISS retrieval + prompt context injection).
- **Panel Defense Q&A**:
  - *Panel Question*: "Why implement RAG instead of simply fine-tuning an LLM on clinical textbooks?"
  - *Defense Response*: "Lewis et al. (2020) demonstrated that RAG outperforms parametric-only models on knowledge-intensive domains for three reasons: (1) **Hallucination Prevention**: The model is conditioned directly on retrieved text excerpts rather than unverified parametric weights; (2) **Auditability**: Every generated coping strategy can be traced to a specific clinical chunk in the DSM-5 or CounselChat; (3) **Zero-Retraining Updates**: When clinical guidelines evolve, we update the FAISS vector index in seconds without expensive GPU model retraining."

---

### 10.3 Supporting Base Paper 2
> **"Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"**  
> *Nils Reimers, Iryna Gurevych (Ubiquitous Knowledge Processing Lab, TU Darmstadt)*  
> **Citation**: EMNLP 2019. [https://arxiv.org/abs/1908.10084](https://arxiv.org/abs/1908.10084)

- **Role in Project**: Provides the mathematical architecture behind our semantic vector search embedding model (`all-MiniLM-L6-v2`).
- **Panel Defense Q&A**:
  - *Panel Question*: "Why did you use Sentence-BERT embeddings instead of TF-IDF, BM25, or raw BERT embeddings?"
  - *Defense Response*: "Reimers & Gurevych (2019) demonstrated that averaging raw BERT token embeddings yields poor semantic representations that perform worse than GloVe. S-BERT fine-tunes BERT using Siamese and Triplet network structures to derive semantically meaningful sentence embeddings where cosine distance directly reflects conceptual similarity. In mental healthcare, users describe distress using colloquial metaphors (*'Everything feels heavy and dark'*); lexical search engines like TF-IDF or BM25 fail because they look for exact keyword overlap, whereas S-BERT matches the underlying psychological meaning to clinical chunks on severe depression."

---

## 11. Conclusion & Future Roadmap

### 11.1 Project Summary
MindCare AI demonstrates a production-ready, academically rigorous mental health support ecosystem specifically optimized for developing nations. By combining:
- Three task-optimized Transformer classifiers (DistilBERT, RoBERTa, DeBERTa-v3),
- Dense clinical vector retrieval over 4,500+ therapist records and WHO/DSM-5 literature,
- Localized multilingual LLM dialogue with Roman Urdu quality filtering,
- Non-generative emergency crisis interceptors, and
- A complete 3-tier REST architecture backed by PostgreSQL connection pooling,

MindCare AI provides an empathetic, culturally-aligned, and privacy-preserving bridge across the psychiatric treatment gap.

### 11.2 Future Roadmap (Next 6–12 Months)
1. **Acoustic Speech Analysis (Multimodal AI)**: Integrate `openSMILE` or `Wav2Vec 2.0` to extract vocal pitch, jitter, and speech cadence from voice messages, fusing audio embeddings with textual features for multimodal stress detection.
2. **Contextual In-Chat Exercise Triggers**: Automatically embed interactive breathing widgets inside the chat pane whenever the stress model outputs a confidence score $> 80\%$.
3. **Psychiatric Summary PDF Export**: Allow users to generate an encrypted 14-day emotional trajectory report formatted for clinical presentation to licensed human psychiatrists.
4. **Mobile Deployment**: Package the frontend as a cross-platform mobile application using Flutter or React Native with on-device SQLite synchronization.

---

*Report prepared by the MindCare AI Development Team — Final Year Project 2026*

