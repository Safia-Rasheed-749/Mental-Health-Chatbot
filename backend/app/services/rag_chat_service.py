# -*- coding: utf-8 -*-
# backend/app/services/rag_chat_service.py
# Multi-turn history is sent as role-specific messages; classifier outputs stay
# separate from the conversational prompt and user-facing response.

"""
RAG Chat Service - Mental Health Chatbot FYP

This service integrates:
1. Emotion / Stress / Depression detection models
2. RAG pipeline (retrieval from knowledge base)
3. LLM (response generation using the current question and relevant context)

Flow for every /chat request:
    user message
        -> run 3 classifiers in parallel (emotion, stress, depression)
        -> retrieve relevant chunks from FAISS vector store
        -> build context string from retrieved chunks
        -> format prompt with role-preserving history and latest question
        -> LLM generates response
        -> return response text + raw detection results
"""

from typing import List, Optional, Tuple
import os
import re
import hashlib

from langchain_core.documents import Document

from app.ai.emotion_detection.predict import predict_emotion
from app.ai.stress_detection.predict import predict_stress
from app.ai.depression_detection.predict import predict_depression
from app.ai.llm.llm import get_llm
from app.ai.llm.prompt import get_prompt, detect_language, resolve_response_language, history_messages
from app.ai.llm.validator import validate_response
from app.ai.rag.embeddings import get_embedding_model
from app.ai.rag.retriever import get_retriever
from app.ai.rag.vector_store import load_vector_store
from .crisis_utils import assess_crisis

# Crisis guardrail (Part 2 integration)
from app.services.crisis_detector import detect_crisis, log_crisis_event
from app.services.crisis_resources import get_crisis_response
from app.services.privacy import redact_sensitive_data
from app.services.chat_output import clean_user_response
from app.services.response_generation import generate_validated_response

# =====================================================
# Configuration
# =====================================================

TOP_K = 4          # Candidate RAG chunks; relevance-filtered before prompting

# =====================================================
# Context Builder
# =====================================================

def build_context(documents: List[Document]) -> str:
    """
    Convert retrieved documents into a formatted context string.

    Args:
        documents: List of Document objects from the retriever.

    Returns:
        Unlabeled context text, or an empty string if there are no relevant passages.
    """
    return "\n\n".join(document.page_content.strip() for document in documents if document.page_content.strip())


def relevant_documents(question: str, documents: List[Document]) -> List[Document]:
    """Keep only documents with meaningful lexical overlap; RAG is optional context."""
    words = {w for w in re.findall(r"[\w\u0600-\u06ff]+", question.lower()) if len(w) > 2}
    if not words:
        return []
    scored = []
    for document in documents:
        content_words = {w for w in re.findall(r"[\w\u0600-\u06ff]+", document.page_content.lower()) if len(w) > 2}
        overlap = len(words & content_words) / max(1, len(words))
        if overlap >= 0.12:
            scored.append((overlap, document))
    return [doc for _, doc in sorted(scored, key=lambda row: row[0], reverse=True)[:2]]


# =====================================================
# Run All Detectors
# =====================================================

def run_detectors(text: str) -> Tuple[dict, dict, dict]:
    """
    Run the emotion, stress, and depression classifiers on the user's message.

    The calls are sequential (all models are in-process PyTorch models;
    no async benefit here).  They are kept in one function to make it
    easy to parallelise later with a ThreadPoolExecutor if needed.

    Args:
        text: Raw user message.

    Returns:
        Tuple of (emotion_result, stress_result, depression_result).
    """
    emotion_result    = predict_emotion(text)
    stress_result     = predict_stress(text)
    depression_result = predict_depression(text)
    return emotion_result, stress_result, depression_result


# =====================================================
# RAG Chat Initialization
# =====================================================

def initialize_rag_chat():
    """
    Initialize RAG + LLM components once at module load time.

    Steps:
        1. Load embedding model  (all-MiniLM-L6-v2)
        2. Load FAISS vector store from disk
        3. Create retriever
        4. Load LLM  (ChatOllama / llama3.2:1b)

    Note:
        Prompt is no longer pre-loaded here — it is chosen
        per-request based on detected language.

    Returns:
        tuple: (retriever, llm)
    """
    print("Initializing RAG Chat Service...")

    print("  Loading embedding model...")
    embeddings = get_embedding_model()

    print("  Loading vector store...")
    vector_store = load_vector_store(embeddings)

    print(f"  Creating retriever (top_k={TOP_K})...")
    retriever = get_retriever(
        vector_store=vector_store,
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )

    print("  Loading LLM...")
    llm = get_llm()

    print("RAG Chat Service initialized successfully.")
    return retriever, llm


# =====================================================
# LLM Call + Validation + Regenerate
# =====================================================

def _invoke_and_validate(
    messages: list,
    question: str,
    language: str,
) -> tuple[str, bool]:
    """
    Invoke the LLM, validate the response, and regenerate
    once if validation fails.

    Args:
        messages:  Formatted LangChain message list.
        question:  Original user message (for correction prompt).
        language:  Detected language ("english"/"roman_urdu"/"urdu").

    Returns:
        (response_text, was_regenerated)
            response_text   — final response string
            was_regenerated — True if a regeneration was needed
    """
    response_text, regenerated = generate_validated_response(llm, messages, question, language)
    validation = validate_response(response_text, language)
    print(f"  Validation {'PASSED' if validation['valid'] else 'FALLBACK'} (language={language})")
    return response_text, regenerated


# Initialize once when the module is first imported.
# All subsequent requests reuse the same warm instances.
retriever, llm = initialize_rag_chat()


# =====================================================
# Main Chat Function
# =====================================================

def generate_chat_response(
    question: str,
    history: Optional[list] = None,
    response_language: str = "auto",
    input_language: Optional[str] = None,
    input_mode: str = "text",
) -> dict:
    """
    Generate a response using detectors + RAG + LLM.

    Full pipeline:
        1. Run emotion / stress / depression classifiers
        2. Retrieve relevant chunks from FAISS
        3. Build mental_state string from classifier outputs
        4. Build context string from retrieved chunks
        5. Format history prefix (last MAX_HISTORY_TURNS turns, token-budgeted)
        6. Format prompt  (context + mental_state + history + question)
        7. Generate LLM response
        8. Return response text together with raw detection scores

    Args:
        question: User's current message.
        history:  Optional list of previous turns as ChatMessage objects or
                  plain dicts with 'role' and 'content' keys.
                  None or empty → stateless behaviour (same as before).

    Returns:
        dict with keys:
            response           (str)   – LLM-generated reply
            emotion            (str)   – detected emotion label
            emotion_confidence (float) – confidence %
            stress             (str)   – "Stress" | "No Stress"
            stress_confidence  (float)
            depression         (str)   – "Depression" | "No Depression"
            depression_confidence (float)
    """
    detected_language = input_language if input_language in {"english", "roman_urdu", "urdu"} else detect_language(question)
    language = resolve_response_language(question, response_language, input_language, history)
    if os.getenv("MINDCARE_ENV", "production").lower() == "development":
        print(
            f"[chat-dev] input_language={detected_language}; transcript={question!r}; "
            f"requested_output={language}; input_mode={input_mode}"
        )

    # ============================================
    # CRISIS GUARDRAIL — MUST BE FIRST CHECK
    # Bypasses all RAG/LLM calls if crisis detected
    # ============================================
    crisis_result = detect_crisis(question)
    if crisis_result["is_crisis"]:
        log_crisis_event(
            severity=crisis_result["severity"],
            matched_phrases=crisis_result["matched_phrases"],
            language=language,
        )
        crisis_response = get_crisis_response(
            severity=crisis_result["severity"],
            language=language,
        )
        print(
            f"🚨 CRISIS DETECTED — Severity: {crisis_result['severity']} | "
            f"Language: {crisis_result['language']} | "
            f"Bypassing LLM, returning helpline template"
        )
        return {
            "response":              crisis_response,
            "crisis":                True,
            "severity":              crisis_result["severity"],
            "emotion":               None,
            "emotion_confidence":    0.0,
            "stress":                None,
            "stress_confidence":     0.0,
            "depression":            None,
            "depression_confidence": 0.0,
            "language": language,
            "speech_text": (
                get_crisis_response(crisis_result["severity"], "urdu")
                if input_mode == "speech" and language == "roman_urdu"
                else crisis_response if input_mode == "speech" else ""
            ),
        }
    # ============================================
    # NORMAL FLOW (existing code continues below)
    # ============================================

    # Crisis detection intentionally used the original message above. All
    # normal model and retrieval work uses the privacy-redacted version.
    question = redact_sensitive_data(question)

    # --------------------------------------------------
    # Step 1: Detect language (Python-side — reliable)
    # --------------------------------------------------
    print(f"  Detected language: {language}")

    # --------------------------------------------------
    # Step 1.5: Immediate Crisis Guardrail Check
    # --------------------------------------------------
    crisis_eval = assess_crisis(question, language)
    if crisis_eval["is_crisis"]:
        # Use level if provided, otherwise default to "high"
        level = crisis_eval.get("level", "high")
        print(f"  [CRISIS DETECTED]: level={level} — activating safety protocol.")
        try:
            emotion_result, stress_result, depression_result = run_detectors(question)
        except Exception:
            emotion_result = {"emotion": None, "confidence": None}
            stress_result = {"stress": None, "confidence": None}
            depression_result = {"depression": None, "confidence": None}

        return {
            "response": crisis_eval["response"],
            "emotion": emotion_result["emotion"],
            "emotion_confidence": emotion_result["confidence"],
            "stress": stress_result["stress"],
            "stress_confidence": stress_result["confidence"],
            "depression": depression_result["depression"],
            "depression_confidence": depression_result["confidence"],
            "crisis": True,
            "crisis_level": level,
            "language": language,
            "speech_text": (
                get_crisis_response(level, "urdu")
                if input_mode == "speech" and language == "roman_urdu"
                else crisis_eval["response"] if input_mode == "speech" else ""
            ),
        }

    # --------------------------------------------------
    # Step 2: Run all three classifiers
    # --------------------------------------------------
    emotion_result, stress_result, depression_result = run_detectors(question)

    print(
        f"  Detected — emotion: {emotion_result['emotion']} "
        f"({emotion_result['confidence']:.1f}%), "
        f"stress: {stress_result['stress']} "
        f"({stress_result['confidence']:.1f}%), "
        f"depression: {depression_result['depression']} "
        f"({depression_result['confidence']:.1f}%)"
    )

    # --------------------------------------------------
    # Step 3: Retrieve relevant documents from FAISS
    # --------------------------------------------------
    documents = relevant_documents(question, retriever.invoke(question))

    # --------------------------------------------------
    # Step 4: Build context and mental_state strings
    # --------------------------------------------------
    context      = build_context(documents)

    # --------------------------------------------------
    # Step 5: Keep history as role-specific messages, separate from the latest question.
    # --------------------------------------------------
    prompt = get_prompt(language)
    messages = prompt.format_messages(
        context=context,
        history=history_messages(history),
        question=question,
    )

    # --------------------------------------------------
    # Step 6: Generate LLM response + validate/regenerate
    # --------------------------------------------------
    response_text, regenerated = _invoke_and_validate(messages, question, language)
    response_text = clean_user_response(response_text, language, context, question)

    speech_text = response_text if input_mode == "speech" else ""
    if input_mode == "speech" and language == "roman_urdu":
        try:
            from app.voice.speech import roman_urdu_to_urdu
            speech_text = roman_urdu_to_urdu(response_text)
            speech_validation = validate_response(speech_text, "urdu")
            if not speech_validation["valid"]:
                speech_text = ""
        except Exception as exc:
            print(f"  Urdu speech rendering unavailable: {exc}")
            speech_text = ""

    if os.getenv("MINDCARE_ENV", "production").lower() == "development":
        print(f"[chat-dev] displayed_response={response_text!r}; tts_input={speech_text!r}")

    if regenerated:
        print("  Note: response was regenerated due to quality check.")

    print("Response generated successfully.")

    # --------------------------------------------------
    # Step 7: Return enriched result
    # --------------------------------------------------
    return {
        "response":              response_text,
        "crisis":                False,
        "severity":              None,
        "emotion":               emotion_result["emotion"],
        "emotion_confidence":    emotion_result["confidence"],
        "stress":                stress_result["stress"],
        "stress_confidence":     stress_result["confidence"],
        "depression":            depression_result["depression"],
        "depression_confidence": depression_result["confidence"],
        "crisis":                False,
        "crisis_level":          "none",
        "language":              language,
        "speech_text":           speech_text,
    }


# =====================================================
# Helper Functions
# =====================================================

def get_retrieved_chunks(question: str) -> List[Document]:
    """
    Return raw retrieved chunks without generating a response.
    Useful for debugging and offline evaluation.
    """
    return retriever.invoke(question)


def generate_response_with_context(question: str) -> dict:
    """
    Generate a response and return the full intermediate data.
    Useful for evaluation pipelines.

    Returns:
        dict with: question, response, context, mental_state,
                   retrieved_chunks, emotion_result,
                   stress_result, depression_result
    """
    emotion_result, stress_result, depression_result = run_detectors(question)

    language     = detect_language(question)
    documents    = relevant_documents(question, retriever.invoke(question))
    context      = build_context(documents)

    prompt   = get_prompt(language)
    messages = prompt.format_messages(
        context=context,
        history=[],
        question=question,
    )

    raw_response = llm.invoke(messages)
    raw_content = getattr(raw_response, "content", raw_response)
    if isinstance(raw_content, list):
        raw_text = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in raw_content
        ).strip()
    else:
        raw_text = str(raw_content).strip()
    prompt_bytes = "\n".join(
        f"{message.type}:{message.content}" for message in messages
    ).encode("utf-8")
    retrieved_chunks = []
    for document in documents:
        metadata = dict(document.metadata or {})
        chunk_text = document.page_content or ""
        stable_source = str(metadata.get("source", metadata.get("file_path", "unknown")))
        stable_page = str(metadata.get("page", ""))
        content_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
        retrieved_chunks.append({
            "chunk_id": hashlib.sha256(
                f"{stable_source}\0{stable_page}\0{content_hash}".encode("utf-8")
            ).hexdigest()[:20],
            "source": stable_source,
            "page": metadata.get("page"),
            "content_sha256": content_hash,
            "text": chunk_text,
        })

    return {
        "question":          question,
        "response":          clean_user_response(raw_text, language, context, question),
        "raw_response":      raw_text,
        "context":           context,
        "retrieved_chunks":  retrieved_chunks,
        "prompt_sha256":     hashlib.sha256(prompt_bytes).hexdigest(),
        "emotion_result":    emotion_result,
        "stress_result":     stress_result,
        "depression_result": depression_result,
        "language":          language,
    }


# =====================================================
# Standalone Test
# =====================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Integrated RAG + Detector Chat Service")
    print("=" * 60)

    test_queries = [
        "I have been feeling really low and empty lately. Can you help me?",
        "I feel like nobody understands me and I am completely alone.",
        "I had a really bad day and I just need someone to talk to.",
    ]

    for query in test_queries:
        print(f"\nQuestion: {query}")
        print("-" * 40)
        result = generate_chat_response(query)
        print(f"Emotion    : {result['emotion']} ({result['emotion_confidence']:.1f}%)")
        print(f"Stress     : {result['stress']} ({result['stress_confidence']:.1f}%)")
        print(f"Depression : {result['depression']} ({result['depression_confidence']:.1f}%)")
        print(f"Response   :\n{result['response']}")
        print("-" * 40)
