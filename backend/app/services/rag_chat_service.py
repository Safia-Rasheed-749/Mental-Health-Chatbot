# -*- coding: utf-8 -*-
# backend/app/services/rag_chat_service.py
# MODIFIED: Added multi-turn conversation memory support.
#   - Added MAX_HISTORY_TURNS, MAX_HISTORY_TOKENS, MAX_MESSAGE_CHARS config
#   - Added format_history() helper
#   - Updated generate_chat_response() to accept optional history parameter
#   - History is injected as a prefix in the question slot (no prompt.py changes)
#   - All existing RAG, detector, safety, and language logic is unchanged

"""
RAG Chat Service - Mental Health Chatbot FYP

This service integrates:
1. Emotion / Stress / Depression detection models
2. RAG pipeline (retrieval from knowledge base)
3. LLM (response generation using retrieved context + detected mental state)

Flow for every /chat request:
    user message
        -> run 3 classifiers in parallel (emotion, stress, depression)
        -> retrieve relevant chunks from FAISS vector store
        -> build mental_state string from classifier results
        -> build context string from retrieved chunks
        -> format history prefix (last N turns, token-budgeted)
        -> format prompt  (context + mental_state + history + question)
        -> LLM generates response
        -> return response text + raw detection results
"""

from typing import List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import json
import re

from langchain_core.documents import Document

from app.ai.emotion_detection.predict import predict_emotion
from app.ai.stress_detection.predict import predict_stress
from app.ai.depression_detection.predict import predict_depression
from app.ai.llm.llm import get_llm
from app.ai.llm.prompt import get_prompt, detect_language
from app.ai.llm.validator import validate_response, build_correction_prompt
from app.ai.llm.roman_urdu_style import MAX_REGENERATE_ATTEMPTS
from app.ai.rag.embeddings import get_embedding_model
from app.ai.rag.retriever import get_retriever
from app.ai.rag.vector_store import load_vector_store
from .crisis_utils import assess_crisis

# Crisis guardrail (Part 2 integration)
from app.services.crisis_detector import detect_crisis, log_crisis_event
from app.services.crisis_resources import get_crisis_response
from app.services.privacy import redact_sensitive_data
from app.database.connection import db_cursor

# =====================================================
# Configuration
# =====================================================

TOP_K = 4          # Number of RAG chunks to retrieve
LOW_CONF = 60.0    # Confidence threshold below which a label is "unreliable"

# --- Multi-turn memory configuration (change these to tune behaviour) ---
MAX_HISTORY_TURNS  = 1     # Maximum previous turns to inject (1 turn = 1 user + 1 assistant)
MAX_HISTORY_TOKENS = 1500  # Approximate token budget for history (1 token ≈ 4 chars)
MAX_MESSAGE_CHARS  = 500   # Truncate any single message longer than this

_JOURNAL_STOPWORDS = {
    "about", "after", "also", "am", "and", "are", "because", "been", "being",
    "but", "for", "from", "have", "her", "his", "into", "its", "just", "like",
    "more", "much", "my", "our", "that", "the", "their", "them", "there", "this",
    "was", "were", "with", "would", "you", "your",
}
_JOURNAL_SYNONYM_GROUPS = (
    {"anxious", "anxiety", "nervous", "nervousness", "worried", "worry", "worrying"},
    {"exam", "exams", "fyp", "presentation", "project", "study", "studies", "studying"},
    {"tired", "fatigue", "exhausted", "sleep", "sleeping", "energy"},
    {"stress", "stressed", "pressure", "overwhelmed", "overwhelm"},
)


def _journal_terms(text: str) -> set[str]:
    return {
        word for word in re.findall(r"[a-z]+", text.lower())
        if len(word) >= 4 and word not in _JOURNAL_STOPWORDS
    }


def _journal_topics(text: str) -> set[str]:
    words = set(re.findall(r"[a-z]+", text.lower()))
    return {
        f"topic_{index}"
        for index, group in enumerate(_JOURNAL_SYNONYM_GROUPS)
        if words & group
    }


def _journal_is_relevant(question: str, journal_text: str) -> bool:
    question_terms = _journal_terms(question)
    journal_terms = _journal_terms(journal_text)
    return bool(
        question_terms & journal_terms
        or _journal_topics(question) & _journal_topics(journal_text)
    )


def _response_mentions_journal(response: str, journal_text: str) -> bool:
    journal_terms = _journal_terms(journal_text)
    if not journal_terms:
        return True
    response_terms = _journal_terms(response)
    shared_terms = len(journal_terms & response_terms)
    shared_topics = len(_journal_topics(response) & _journal_topics(journal_text))
    required_terms = min(2, len(journal_terms))
    return shared_terms + shared_topics >= required_terms

# =====================================================
# Context Builder
# =====================================================

def build_context(documents: List[Document]) -> str:
    """
    Convert retrieved documents into a formatted context string.

    Args:
        documents: List of Document objects from the retriever.

    Returns:
        Formatted context string with numbered chunk headers.
    """
    parts = []
    for index, document in enumerate(documents, start=1):
        parts.append(f"[Chunk {index}]\n{document.page_content}")
    return "\n\n".join(parts)


def mood_to_score(mood: str) -> Optional[int]:
    """Map stored mood labels to their requested 1-5 severity score."""
    return {
        "happy": 5,
        "neutral": 4,
        "anxious": 3,
        "sad": 2,
        "angry": 1,
        "depressed": 1,
    }.get((mood or "").strip().lower())


def build_user_context(user_id: int) -> str:
    """Load and format the user's recent mood and journal history."""
    now = datetime.now()
    cutoff_30 = now - timedelta(days=30)
    cutoff_7 = now - timedelta(days=7)
    with db_cursor() as cur:
        cur.execute(
            "SELECT mood, created_at FROM mood WHERE user_id=%s "
            "AND created_at >= NOW() - INTERVAL '30 days' ORDER BY created_at DESC",
            (user_id,),
        )
        moods = cur.fetchall()
        cur.execute(
            "SELECT entry, created_at FROM journal WHERE user_id=%s "
            "ORDER BY created_at DESC LIMIT 3",
            (user_id,),
        )
        journals = cur.fetchall()

    if not moods and not journals:
        return ""

    scores_30 = []
    scores_7 = []
    recent_moods = []
    for mood, created_at in moods:
        label = str(mood)
        recent_moods.append(label)
        score = mood_to_score(label)
        if score is not None:
            scores_30.append(score)
            if created_at and created_at.replace(tzinfo=None) >= cutoff_7:
                scores_7.append(score)

    def average(scores):
        return f"{sum(scores) / len(scores):.1f}" if scores else "N/A"

    lines = [
        f"- Recent Mood Logs: {', '.join(recent_moods) if recent_moods else 'None'}",
        f"- Mood Trend: Recent (7 days) average is {average(scores_7)}/5. "
        f"Past (30 days) average is {average(scores_30)}/5.",
        "- Recent Journal Entries:",
    ]
    if journals:
        for index, (entry, created_at) in enumerate(journals, start=1):
            entry_date = created_at.strftime("%Y-%m-%d") if created_at else "Unknown date"
            journal_text = str(entry or "")
            json_text = journal_text.removeprefix("JOURNAL_V1:").strip()
            try:
                parsed_entry = json.loads(json_text)
                if isinstance(parsed_entry, dict) and isinstance(parsed_entry.get("content"), str):
                    journal_text = parsed_entry["content"]
            except (json.JSONDecodeError, TypeError):
                pass
            lines.append(f"  {index}. [{entry_date}] {journal_text}")
    else:
        lines.insert(0, "User Context:")
        lines.append("  None")
    return "\n".join(lines)


# =====================================================
# Mental-State Builder
# =====================================================

def build_mental_state(
    emotion_result: dict,
    stress_result: dict,
    depression_result: dict,
) -> str:
    """
    Format classifier outputs into a structured string for the LLM prompt.

    Each entry shows the predicted label and its confidence so the LLM
    can judge reliability.  Labels below LOW_CONF are flagged as
    low-confidence so the model treats them with appropriate scepticism.

    Args:
        emotion_result:    Output of predict_emotion()
        stress_result:     Output of predict_stress()
        depression_result: Output of predict_depression()

    Returns:
        Multi-line string injected into the {mental_state} prompt slot.
    """

    def _fmt(label: str, confidence: float) -> str:
        flag = " (low confidence — treat as unreliable)" if confidence < LOW_CONF else ""
        return f"{label} ({confidence:.1f}%{flag})"

    lines = [
        "Detected Mental State:",
        f"  Emotion    : {_fmt(emotion_result['emotion'],       emotion_result['confidence'])}",
        f"  Stress     : {_fmt(stress_result['stress'],         stress_result['confidence'])}",
        f"  Depression : {_fmt(depression_result['depression'], depression_result['confidence'])}",
    ]
    return "\n".join(lines)


# =====================================================
# History Formatter
# =====================================================

def format_history(history: Optional[list]) -> str:
    """
    Format conversation history into a plain-text prefix for the prompt.

    Rules applied (in order):
        1. None / empty → return ""
        2. Keep only the last MAX_HISTORY_TURNS turns
        3. Truncate each message to MAX_MESSAGE_CHARS characters
        4. Stop adding turns (oldest-first) once MAX_HISTORY_TOKENS budget exceeded
        5. Skip any malformed entries (missing role/content) silently

    A 'turn' is one user message + one assistant reply (2 list entries).
    The history list is assumed to be chronological (oldest first).

    Args:
        history: List of dicts or ChatMessage objects with .role and .content

    Returns:
        Formatted string like:
            "Previous conversation:\nUser: ...\nAssistant: ...\n\n"
        or "" if nothing valid to inject.
    """
    if not history:
        return ""

    # Normalise: accept both Pydantic models and plain dicts
    turns = []
    for entry in history:
        try:
            role    = entry.role    if hasattr(entry, "role")    else entry["role"]
            content = entry.content if hasattr(entry, "content") else entry["content"]
            if role not in ("user", "assistant") or not isinstance(content, str):
                continue
            turns.append((role, content.strip()))
        except (KeyError, AttributeError, TypeError):
            continue  # skip malformed entries

    if not turns:
        return ""

    crisis_markers = (
        "0311-7786264", "0800-22444", "1166", "988", "1122", "741741",
        "i hear how much pain", "please reach out to a trained professional",
    )
    filtered_turns = []
    index = 0
    while index < len(turns):
        role, content = turns[index]
        if role == "user" and index + 1 < len(turns) and turns[index + 1][0] == "assistant":
            assistant_content = turns[index + 1][1].lower()
            user_is_crisis = detect_crisis(content)["is_crisis"]
            assistant_is_crisis = any(marker in assistant_content for marker in crisis_markers)
            if not user_is_crisis and not assistant_is_crisis:
                filtered_turns.extend(turns[index:index + 2])
            index += 2
            continue
        filtered_turns.append(turns[index])
        index += 1
    turns = filtered_turns

    if not turns:
        return ""

    # Keep only the last MAX_HISTORY_TURNS*2 entries (each turn = user + assistant)
    max_entries = MAX_HISTORY_TURNS * 2
    turns = turns[-max_entries:]

    # Build lines within token budget (1 token ≈ 4 chars)
    token_budget = MAX_HISTORY_TOKENS * 4  # work in chars for simplicity
    used_chars   = 0
    selected     = []

    for role, content in turns:
        # Truncate long individual messages
        if len(content) > MAX_MESSAGE_CHARS:
            content = content[:MAX_MESSAGE_CHARS] + "…"

        label = "User" if role == "user" else "Assistant"
        line  = f"{label}: {content}"

        if used_chars + len(line) > token_budget:
            break  # budget exhausted — stop (oldest turns dropped first)

        selected.append(line)
        used_chars += len(line)

    if not selected:
        return ""

    injected_turns  = len(selected) // 2 + len(selected) % 2  # rough turn count
    injected_tokens = used_chars // 4
    print(f"  [History] Injected ~{injected_turns} turns (~{injected_tokens} tokens) into prompt.")

    return "Previous conversation:\n" + "\n".join(selected) + "\n\n"


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
    # ── First attempt ──────────────────────────────
    raw = llm.invoke(messages)
    response_text = raw.content if hasattr(raw, "content") else str(raw)

    result = validate_response(response_text, language)

    if result["valid"]:
        print(f"  Validation PASSED (language={language})")
        return response_text, False

    # ── First attempt failed → log and regenerate ──
    print(f"  Validation FAILED (language={language}): {result['reasons']}")

    for attempt in range(1, MAX_REGENERATE_ATTEMPTS + 1):
        print(f"  Regeneration attempt {attempt}/{MAX_REGENERATE_ATTEMPTS}...")

        correction = build_correction_prompt(question, response_text, result)

        # Send correction as a plain human message so the LLM rewrites
        from langchain_core.messages import HumanMessage
        regen_messages = messages + [HumanMessage(content=correction)]

        raw2 = llm.invoke(regen_messages)
        response_text = raw2.content if hasattr(raw2, "content") else str(raw2)

        result2 = validate_response(response_text, language)
        if result2["valid"]:
            print(f"  Regeneration PASSED on attempt {attempt}")
            return response_text, True

        print(f"  Regeneration attempt {attempt} still failed: {result2['reasons']}")
        result = result2   # use latest failure for next correction

    # All attempts exhausted — return best available response
    print("  All regeneration attempts exhausted. Returning last response.")
    return response_text, True


# Initialize once when the module is first imported.
# All subsequent requests reuse the same warm instances.
retriever, llm = initialize_rag_chat()


# =====================================================
# Main Chat Function
# =====================================================

def generate_chat_response(question: str, history: Optional[list] = None, user_id: Optional[int] = None) -> dict:
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
    print(f"Generating response for: {question[:60]}...")

    # ============================================
    # CRISIS GUARDRAIL — MUST BE FIRST CHECK
    # Bypasses all RAG/LLM calls if crisis detected
    # ============================================
    crisis_result = detect_crisis(question)
    if crisis_result["is_crisis"]:
        log_crisis_event(
            severity=crisis_result["severity"],
            matched_phrases=crisis_result["matched_phrases"],
            language=crisis_result["language"],
        )
        crisis_response = get_crisis_response(
            severity=crisis_result["severity"],
            language=crisis_result["language"],
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
    language = detect_language(question)
    print(f"  Detected language: {language}")

    # --------------------------------------------------
    # Step 1.5: Immediate Crisis Guardrail Check
    # --------------------------------------------------
    crisis_eval = assess_crisis(question, language)
    if crisis_eval["is_crisis"]:
        # Use level if provided, otherwise default to "high"
        level = crisis_eval.get("level", "high")
        print(f"  [CRISIS DETECTED]: level={level} — activating safety protocol.")
        return {
            "response": crisis_eval["response"],
            "emotion": None,
            "emotion_confidence": 0.0,
            "stress": None,
            "stress_confidence": 0.0,
            "depression": None,
            "depression_confidence": 0.0,
            "crisis": True,
            "crisis_level": level,
        }

    # Fetch personal history only after both crisis checks have passed.
    try:
        user_context = build_user_context(user_id) if user_id is not None else "User Context: unavailable"
    except Exception as exc:
        print(f"  Could not load user context: {exc}")
        user_context = "User Context: unavailable"

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
    documents = retriever.invoke(question)

    if not documents:
        fallback = {
            "english":    "I don't have enough information to answer that. Please try rephrasing.",
            "roman_urdu": "Mujhe is sawal ka jawab nahi mila. Kripya dobarah try karein.",
            "urdu":       "مجھے اس سوال کا جواب نہیں ملا۔ براہ کرم دوبارہ کوشش کریں۔",
        }
        return {
            "response":              fallback.get(language, fallback["english"]),
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
        }

    # --------------------------------------------------
    # Step 4: Build context and mental_state strings
    # --------------------------------------------------
    context      = build_context(documents)
    mental_state = build_mental_state(emotion_result, stress_result, depression_result)

    # --------------------------------------------------
    # Step 5: Select language-specific prompt and format
    # Keep prior turns separate from the current user question.
    # --------------------------------------------------
    history_context = format_history(history)
    journal_match = re.search(
        r"^\s*\d+\.\s*\[[^\]]+\]\s*(.+)$",
        user_context,
        flags=re.MULTILINE,
    )
    first_journal_text = journal_match.group(1).strip() if journal_match else ""

    prompt = get_prompt(language)
    print(f"  [User Context] user_id={user_id}\n{user_context}")
    messages = prompt.format_messages(
        context=context,
        mental_state=mental_state,
        question=question,
        history=history_context,
        user_context=user_context,
    )

    # --------------------------------------------------
    # Step 6: Generate LLM response + validate/regenerate
    # --------------------------------------------------
    response_text, regenerated = _invoke_and_validate(messages, question, language)

    # Crisis responses exit above; only add this fallback to a normal response
    # when the current question relates to the journal and the model omitted it.
    if (
        first_journal_text
        and _journal_is_relevant(question, first_journal_text)
        and not _response_mentions_journal(response_text, first_journal_text)
    ):
        response_text = (
            f"I can see from your recent journal that you wrote: '{first_journal_text}'. "
            "It makes complete sense that you are feeling this way.\n\n"
            + response_text
        )

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
    documents    = retriever.invoke(question)
    context      = build_context(documents)
    mental_state = build_mental_state(emotion_result, stress_result, depression_result)

    prompt   = get_prompt(language)
    messages = prompt.format_messages(
        context=context,
        mental_state=mental_state,
        question=question,
        history="",
        user_context="User Context: unavailable",
    )

    raw_response  = llm.invoke(messages)
    response_text = (
        raw_response.content
        if hasattr(raw_response, "content")
        else str(raw_response)
    )

    return {
        "question":          question,
        "response":          response_text,
        "context":           context,
        "mental_state":      mental_state,
        "retrieved_chunks":  documents,
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
