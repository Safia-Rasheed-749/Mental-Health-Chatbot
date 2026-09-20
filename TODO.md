# RAG Foundation Boilerplate — Task List

## Goal
Prepare the RAG foundation for the AI Mental Health Chatbot:
- Modular document loader (PDFs + web URLs)
- Reusable HuggingFace embeddings module
- FAISS vector store with create / load / save
- Configurable retriever
- Pipeline that only connects the components and returns a retriever
- Separate `backend/knowledge_base/` data folder

## Tasks

- [x] 1. Create `backend/knowledge_base/` directory structure
  - [x] `pdfs/WHO/`
  - [x] `pdfs/CBT/`
  - [x] `pdfs/DSM5/`
  - [x] `pdfs/Psychotherapy/`
  - [x] `web_urls/urls.txt`
  - [x] `processed/`
  - [x] `vector_store/`

- [x] 2. Implement `backend/app/ai/rag/loader.py`
  - [x] `load_pdf_documents()` — recursive scan of `knowledge_base/pdfs/`
  - [x] `load_web_documents()` — reads `web_urls/urls.txt` (skips blank lines & `#`)
  - [x] `load_all_documents()` — combine both
  - [x] Uses LangChain loaders, returns `List[Document]`

- [x] 3. Implement `backend/app/ai/rag/embeddings.py`
  - [x] `get_embedding_model()` — HuggingFace, configurable model name

- [x] 4. Implement `backend/app/ai/rag/vector_store.py`
  - [x] `create_vector_store()`
  - [x] `save_vector_store()`
  - [x] `load_vector_store()`
  - [x] Persist to `knowledge_base/vector_store/`

- [x] 5. Implement `backend/app/ai/rag/retriever.py`
  - [x] `get_retriever()` — configurable, no QA logic

- [x] 6. Implement `backend/app/ai/rag/pipeline.py`
  - [x] Expose `load_all_documents()`, `split_documents()`, `get_embedding_model()`, `create/load_vector_store()`, `get_retriever()`
  - [x] No auto create/load decision, no LLM

- [x] 7. Verify syntax with `python -m py_compile`
- [x] 8. Verified imports & FAISS API against `backend/venv` (langchain-community 0.4.2)

---

# RAG + LLM Integration — Task List

## Goal
Wire the existing RAG retrieval layer to the local Llama 3.2 1B model via Ollama:
User question → Retriever → Context → Prompt → Local LLM → Grounded response.

## Tasks

- [x] 1. Create `backend/app/ai/llm/prompt.py`
  - [x] `get_prompt()` returns a `ChatPromptTemplate` with `{context}` and `{question}`
  - [x] Grounded-answering instructions (no invention, no diagnosis, no fake credentials, insufficiency handling)
  - [x] No model invocation inside prompt.py

- [x] 2. Create `backend/app/ai/llm/test_llm.py`
  - [x] Uses `get_llm()` from existing `llm.py`
  - [x] Sends one simple test message and prints the response
  - [x] Clear error handling (Ollama down, model missing)
  - [x] Runnable via `python -m app.ai.llm.test_llm`

- [x] 3. Create `backend/app/ai/llm/test_rag_llm.py`
  - [x] Loads embeddings, existing FAISS store, retriever (k=4), LLM, prompt
  - [x] Retrieves top-k chunks, builds context, invokes LLM
  - [x] Prints question, retrieved sources, generated response
  - [x] Clear error handling (store missing, retrieval fail, no docs, LLM fail)
  - [x] Does NOT rebuild store / embeddings / integrate FastAPI
  - [x] Runnable via `python -m app.ai.llm.test_rag_llm`

- [x] 4. Add `langchain-ollama` to `backend/requirements.txt` (required by `llm.py`)

- [ ] 5. Install `langchain-ollama` in the venv (manual, per user)
- [ ] 6. Run `python -m app.ai.llm.test_llm`
- [ ] 7. Run `python -m app.ai.llm.test_rag_llm`

