# -*- coding: utf-8 -*-
# backend/app/services/rag_chat_service.py

"""
RAG Chat Service - MindCare AI FYP

Integrates:
  1. Emotion / Stress / Depression detection models (parallel execution)
  2. FAISS RAG knowledge-base retrieval
  3. Per-user mood + journal context integration
  4. Crisis guardrail (keyword-based, deterministic bypass of LLM)
  5. Local LLM response generation (llama3.2 via Ollama)
  6. Multilingual prompt engine (English / Roman Urdu / Urdu script)
  7. Sentence completeness enforcement (zero mid-sentence cut-offs)
  8. Natural opening phrase variation (anti-repetition safeguards)
"""

from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import json
import os
import re

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage

from app.ai.emotion_detection.predict    import predict_emotion
from app.ai.stress_detection.predict     import predict_stress
from app.ai.depression_detection.predict import predict_depression

from app.ai.llm.llm     import get_llm
from app.ai.llm.prompt  import get_prompt, detect_language, resolve_response_language
from app.ai.llm.validator import validate_response, build_correction_prompt

from app.ai.rag.embeddings   import get_embedding_model
from app.ai.rag.retriever    import get_retriever
from app.ai.rag.vector_store import load_vector_store

from app.services.crisis_detector  import detect_crisis, log_crisis_event
from app.services.crisis_resources import get_crisis_response
from app.services.crisis_utils     import assess_crisis
from app.services.privacy          import redact_sensitive_data
from app.database.connection       import db_cursor


# =====================================================
# Configuration
# =====================================================

TOP_K            = 4      # RAG chunks to retrieve
LOW_CONF         = 60.0   # confidence % below which a label is flagged "unreliable"

MAX_HISTORY_TURNS  = 3    # previous turns to include in prompt (3 turns = 6 messages)
MAX_HISTORY_TOKENS = 1500
MAX_MESSAGE_CHARS  = 500


# =====================================================
# Journal / user-context helpers
# =====================================================

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


def _journal_terms(text: str) -> set:
    return {
        word for word in re.findall(r"[a-z]+", text.lower())
        if len(word) >= 4 and word not in _JOURNAL_STOPWORDS
    }


def _journal_topics(text: str) -> set:
    words = set(re.findall(r"[a-z]+", text.lower()))
    return {
        f"topic_{i}"
        for i, group in enumerate(_JOURNAL_SYNONYM_GROUPS)
        if words & group
    }


def _journal_is_relevant(question: str, journal_text: str) -> bool:
    return bool(
        _journal_terms(question) & _journal_terms(journal_text)
        or _journal_topics(question) & _journal_topics(journal_text)
    )


def _response_mentions_journal(response: str, journal_text: str) -> bool:
    journal_terms = _journal_terms(journal_text)
    if not journal_terms:
        return True
    shared_terms  = len(journal_terms & _journal_terms(response))
    shared_topics = len(_journal_topics(response) & _journal_topics(journal_text))
    return shared_terms + shared_topics >= min(2, len(journal_terms))


def mood_to_score(mood: str) -> Optional[int]:
    return {
        "happy": 5, "neutral": 4, "anxious": 3,
        "sad": 2,   "angry": 1,   "depressed": 1,
    }.get((mood or "").strip().lower())


def build_user_context(user_id: int) -> str:
    """Load and format the user's recent mood and journal history."""
    now       = datetime.now()
    cutoff_7  = now - timedelta(days=7)
    cutoff_30 = now - timedelta(days=30)

    try:
        with db_cursor() as cur:
            cur.execute(
                "SELECT mood, created_at FROM mood "
                "WHERE user_id = %s AND created_at >= %s "
                "ORDER BY created_at DESC LIMIT 30",
                (user_id, cutoff_30),
            )
            mood_rows = cur.fetchall()

            cur.execute(
                "SELECT entry, created_at FROM journal "
                "WHERE user_id = %s ORDER BY created_at DESC LIMIT 3",
                (user_id,),
            )
            journals = cur.fetchall()
    except Exception as exc:
        print(f"  [build_user_context] DB error: {exc}")
        return ""

    recent_moods = [r[0] for r in mood_rows[:5]]
    scores_7     = [mood_to_score(r[0]) for r in mood_rows if r[1] and r[1].replace(tzinfo=None) >= cutoff_7 and mood_to_score(r[0]) is not None]
    scores_30    = [mood_to_score(r[0]) for r in mood_rows if mood_to_score(r[0]) is not None]

    def avg(scores):
        return f"{sum(scores)/len(scores):.1f}" if scores else "N/A"

    lines = [
        "User Context:",
        f"- Recent Mood Logs: {', '.join(recent_moods) if recent_moods else 'None'}",
        f"- Mood Trend: 7-day avg {avg(scores_7)}/5 | 30-day avg {avg(scores_30)}/5.",
        "- Recent Journal Entries:",
    ]
    if journals:
        for i, (entry, created_at) in enumerate(journals, 1):
            entry_date  = created_at.strftime("%Y-%m-%d") if created_at else "Unknown"
            journal_text = str(entry or "")
            json_text    = journal_text.removeprefix("JOURNAL_V1:").strip()
            try:
                parsed = json.loads(json_text)
                if isinstance(parsed, dict) and isinstance(parsed.get("content"), str):
                    journal_text = parsed["content"]
            except (json.JSONDecodeError, TypeError):
                pass
            lines.append(f"  {i}. [{entry_date}] {journal_text}")
    else:
        lines.append("  None")

    return "\n".join(lines)


# =====================================================
# Context Builder
# =====================================================

def build_context(documents: List[Document]) -> str:
    return "\n\n".join(
        doc.page_content.strip() for doc in documents if doc.page_content.strip()
    )


# =====================================================
# Mental-State Builder
# =====================================================

def build_mental_state(
    emotion_result:    dict,
    stress_result:     dict,
    depression_result: dict,
) -> str:
    def _fmt(label: str, confidence: float) -> str:
        flag = " (low confidence — treat as unreliable)" if confidence < LOW_CONF else ""
        return f"{label} ({confidence:.1f}%{flag})"

    return "\n".join([
        "Detected Mental State:",
        f"  Emotion    : {_fmt(emotion_result['emotion'],       emotion_result['confidence'])}",
        f"  Stress     : {_fmt(stress_result['stress'],         stress_result['confidence'])}",
        f"  Depression : {_fmt(depression_result['depression'], depression_result['confidence'])}",
    ])


# =====================================================
# History Formatter & Opener Extraction
# =====================================================

def get_last_assistant_opener(history: Optional[list]) -> str:
    """Extract first 4 words of the last assistant message to prevent repeating openers."""
    if not history:
        return ""
    for entry in reversed(history):
        role    = entry.role if hasattr(entry, "role") else (entry.get("role") if isinstance(entry, dict) else None)
        content = entry.content if hasattr(entry, "content") else (entry.get("content") if isinstance(entry, dict) else None)
        if role == "assistant" and isinstance(content, str) and content.strip():
            words = content.strip().split()[:4]
            return " ".join(words)
    return ""


def format_history(history: Optional[list]) -> Tuple[str, str]:
    """
    Return:
        (history_prefix_string, last_assistant_opener)
    """
    if not history:
        return "", ""

    turns = []
    for entry in history:
        try:
            role    = entry.role    if hasattr(entry, "role")    else entry["role"]
            content = entry.content if hasattr(entry, "content") else entry["content"]
            if role not in ("user", "assistant") or not isinstance(content, str):
                continue
            turns.append((role, content.strip()))
        except (KeyError, AttributeError, TypeError):
            continue

    if not turns:
        return "", ""

    # Filter out crisis turns from history
    crisis_markers = (
        "0311-7786264", "0800-22444", "1166", "988", "1122", "741741",
        "i hear how much pain", "please reach out to a trained professional",
    )
    filtered, i = [], 0
    while i < len(turns):
        role, content = turns[i]
        if role == "user" and i + 1 < len(turns) and turns[i + 1][0] == "assistant":
            asst = turns[i + 1][1].lower()
            if not detect_crisis(content)["is_crisis"] and not any(m in asst for m in crisis_markers):
                filtered.extend(turns[i:i + 2])
            i += 2
        else:
            filtered.append(turns[i])
            i += 1

    turns = filtered[-MAX_HISTORY_TURNS * 2:]

    budget, used, selected = MAX_HISTORY_TOKENS * 4, 0, []
    for role, content in turns:
        if len(content) > MAX_MESSAGE_CHARS:
            content = content[:MAX_MESSAGE_CHARS] + "…"
        line = f"{'User' if role == 'user' else 'Assistant'}: {content}"
        if used + len(line) > budget:
            break
        selected.append(line)
        used += len(line)

    if not selected:
        return "", ""

    last_opener = get_last_assistant_opener(history)
    print(f"  [History] Injected {len(selected)//2 + len(selected)%2} turns into prompt. Last opener: {last_opener!r}")

    history_str = "Previous conversation:\n" + "\n".join(selected) + "\n"
    if last_opener:
        history_str += f"[Instruction: Previous response began with: \"{last_opener}...\". Vary your opening phrase and tone naturally. Do NOT start with the same pattern.]\n"
    history_str += "\n"

    return history_str, last_opener


# =====================================================
# Detectors (Parallel Execution)
# =====================================================

def run_detectors(text: str) -> Tuple[dict, dict, dict]:
    """Execute emotion, stress, and depression classifiers concurrently across worker threads."""
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_emotion    = executor.submit(predict_emotion, text)
        f_stress     = executor.submit(predict_stress, text)
        f_depression = executor.submit(predict_depression, text)

        emotion_res    = f_emotion.result()
        stress_res     = f_stress.result()
        depression_res = f_depression.result()

    return emotion_res, stress_res, depression_res


# =====================================================
# RAG + LLM Initialization
# =====================================================

def initialize_rag_chat():
    print("Initializing RAG Chat Service...")
    embeddings   = get_embedding_model()
    vector_store = load_vector_store(embeddings)
    retriever    = get_retriever(
        vector_store=vector_store,
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )
    llm = get_llm()
    print("RAG Chat Service initialized successfully.")
    return retriever, llm


retriever, llm = initialize_rag_chat()


# =====================================================
# LLM Response Processing & Quality Refinement
# =====================================================

def _response_text(result) -> str:
    content = getattr(result, "content", result)
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        ).strip()
    return str(content).strip()


def refine_formulaic_openers(text: str, language: str = "english") -> str:
    """
    Eliminate repetitive formulaic openings if the model outputs them,
    re-orienting the first sentence directly into natural conversation.
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    text = text.strip()

    if language == "english":
        patterns = [
            (r"^It sounds like you(?:'re|\s+are)\s+(?:feeling\s+)?", "Feeling "),
            (r"^It sounds like\s+", ""),
            (r"^It seems like you(?:'re|\s+are)\s+(?:feeling\s+)?", "Feeling "),
            (r"^It seems like\s+", ""),
            (r"^It seems that\s+", ""),
            (r"^I understand that you(?:'re|\s+are)\s+(?:feeling\s+)?", "Feeling "),
            (r"^I understand that\s+", ""),
            (r"^I can see that you(?:'re|\s+are)\s+(?:feeling\s+)?", "Feeling "),
            (r"^I can see that\s+", ""),
            (r"^I hear how much\s+", "That is a lot of "),
            (r"^I hear that\s+", ""),
            (r"^I'm so sorry to hear that\s+", "That sounds really heavy. "),
            (r"^I am so sorry to hear that\s+", "That sounds really heavy. "),
        ]
        for pat, repl in patterns:
            if re.search(pat, text, re.IGNORECASE):
                text = re.sub(pat, repl, text, count=1, flags=re.IGNORECASE).strip()
                if text:
                    text = text[0].upper() + text[1:]
                break

    elif language == "roman_urdu":
        patterns = [
            (r"^Main samajh sakta hoon ke aap\s+", "Aap "),
            (r"^Main samajh sakti hoon ke aap\s+", "Aap "),
            (r"^Main samajh sakta hoon ke\s+", ""),
            (r"^Main samajh sakti hoon ke\s+", ""),
            (r"^Mujhe afsos hai ke aap\s+", "Aap "),
            (r"^Mujhe afsos hai ke\s+", ""),
            (r"^Aisa lagta hai ke aap\s+", "Aap "),
            (r"^Aisa lagta hai ke\s+", ""),
            (r"^Main dekh sakta hoon ke\s+", ""),
        ]
        for pat, repl in patterns:
            if re.search(pat, text, re.IGNORECASE):
                text = re.sub(pat, repl, text, count=1, flags=re.IGNORECASE).strip()
                if text:
                    text = text[0].upper() + text[1:]
                break

    elif language == "urdu":
        patterns = [
            (r"^میں سمجھ سکتا ہوں کہ آپ\s+", "آپ "),
            (r"^میں سمجھ سکتی ہوں کہ آپ\s+", "آپ "),
            (r"^میں سمجھ سکتا ہوں کہ\s+", ""),
            (r"^میں سمجھ سکتی ہوں کہ\s+", ""),
            (r"^مجھے افسوس ہے کہ آپ\s+", "آپ "),
            (r"^مجھے افسوس ہے کہ\s+", ""),
            (r"^ایسا لگتا ہے کہ آپ\s+", "آپ "),
            (r"^ایسا لگتا ہے کہ\s+", ""),
        ]
        for pat, repl in patterns:
            if re.search(pat, text):
                text = re.sub(pat, repl, text, count=1).strip()
                break

    return text


def ensure_complete_sentences(text: str, language: str = "english") -> str:
    """
    Ensure every response ends with a complete sentence.
    Detects and cleanly trims incomplete, dangling trailing clauses
    back to the last finished sentence.
    Supports English, Roman Urdu, and Urdu Unicode script (۔, ؟).
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    text = text.strip()

    terminal_chars = {".", "?", "!", '"', "'", ")", "۔", "؟", "”", "’"}

    if text and text[-1] in terminal_chars:
        return text

    # Split into sentence-like segments
    sentence_pattern = r"(?<=[.?!۔؟])\s+"
    parts = re.split(sentence_pattern, text)

    if len(parts) > 1:
        last_part = parts[-1].strip()
        if last_part and last_part[-1] not in terminal_chars:
            trimmed = " ".join(p.strip() for p in parts[:-1] if p.strip())
            if trimmed and trimmed[-1] in terminal_chars:
                return trimmed

    # If there's only one segment or trimming leaves nothing:
    dangling_connectors = {
        "and", "but", "or", "because", "which", "so", "that", "with", "to", "if",
        "aur", "lekin", "ya", "ke", "toh", "agar", "bhi", "kar", "hoga", "raha",
        "کہ", "اور", "لیکن", "تو", "اگر", "کیونکہ", "یا"
    }
    words = text.split()
    if words and words[-1].lower() in dangling_connectors:
        words = words[:-1]
        text = " ".join(words).strip()

    if text and text[-1] not in terminal_chars:
        default_punct = "۔" if language == "urdu" else "."
        text = text + default_punct

    return text


def clean_user_response(response: str, language: str = "english", context: str = "", question: str = "") -> str:
    """Clean markdown artifacts, refine repetitive openers, and ensure complete sentences."""
    if not isinstance(response, str):
        return ""
    # Strip markdown code fences & AI prefixes
    response = re.sub(r"^\s*```(?:\w+)?\s*|\s*```\s*$", "", response, flags=re.IGNORECASE)
    response = re.sub(r"^\s*(?:Assistant|AI|مددگار)\s*:\s*", "", response)
    response = response.strip()

    # Refine repetitive formula openers if present
    response = refine_formulaic_openers(response, language)

    # Ensure all sentences are complete and terminated with valid punctuation
    response = ensure_complete_sentences(response, language)

    return response.strip()


def generate_validated_response(llm_instance, messages, question, language):
    result     = _response_text(llm_instance.invoke(messages))
    validation = validate_response(result, language)
    if not validation["valid"]:
        correction     = build_correction_prompt(question, result, validation)
        retry_messages = list(messages) + [HumanMessage(content=correction)]
        result         = _response_text(llm_instance.invoke(retry_messages))
    return result, not validation["valid"]


def _invoke_and_validate(messages, question, language):
    response_text, regenerated = generate_validated_response(llm, messages, question, language)
    validation = validate_response(response_text, language)
    print(f"  Validation {'PASSED' if validation['valid'] else 'FALLBACK'} (language={language})")
    return response_text, regenerated


# =====================================================
# Main Chat Function
# =====================================================

def generate_chat_response(
    question:  str,
    history:   Optional[list] = None,
    user_id:   Optional[int]  = None,
) -> dict:
    """
    Full pipeline:
      Crisis check → classifiers (parallel) → RAG → user context → LLM → validated & complete response
    """
    print(f"Generating response for: {question[:60]}...")

    # ── CRISIS GUARDRAIL (runs on original text, before redaction) ──────
    crisis_result = detect_crisis(question)
    if crisis_result["is_crisis"]:
        log_crisis_event(
            severity=crisis_result["severity"],
            matched_phrases=crisis_result["matched_phrases"],
            language=crisis_result["language"],
        )
        language = detect_language(question)
        print(f"🚨 CRISIS — Severity: {crisis_result['severity']} | Lang: {language}")
        return {
            "response":              get_crisis_response(crisis_result["severity"], language),
            "crisis":                True,
            "severity":              crisis_result["severity"],
            "emotion":               None,
            "emotion_confidence":    0.0,
            "stress":                None,
            "stress_confidence":     0.0,
            "depression":            None,
            "depression_confidence": 0.0,
        }

    # ── PRIVACY REDACTION ────────────────────────────────────────────────
    question = redact_sensitive_data(question)

    # ── LANGUAGE DETECTION ───────────────────────────────────────────────
    language = detect_language(question)
    print(f"  Language: {language}")

    # ── SECONDARY CRISIS CHECK (assess_crisis, post-redaction) ───────────
    crisis_eval = assess_crisis(question, language)
    if crisis_eval["is_crisis"]:
        level = crisis_eval.get("level", "HIGH")
        print(f"  [CRISIS-2] level={level}")
        return {
            "response":              crisis_eval["response"],
            "crisis":                True,
            "severity":              level,
            "emotion":               None,
            "emotion_confidence":    0.0,
            "stress":                None,
            "stress_confidence":     0.0,
            "depression":            None,
            "depression_confidence": 0.0,
        }

    # ── CLASSIFIERS (Parallel execution) ─────────────────────────────────
    emotion_result, stress_result, depression_result = run_detectors(question)
    print(
        f"  emotion={emotion_result['emotion']} ({emotion_result['confidence']:.0f}%) | "
        f"stress={stress_result['stress']} ({stress_result['confidence']:.0f}%) | "
        f"depression={depression_result['depression']} ({depression_result['confidence']:.0f}%)"
    )

    # ── RAG RETRIEVAL ─────────────────────────────────────────────────────
    documents = retriever.invoke(question)
    context   = build_context(documents)

    # ── MENTAL STATE STRING ───────────────────────────────────────────────
    mental_state = build_mental_state(emotion_result, stress_result, depression_result)

    # ── USER CONTEXT (mood/journal) ───────────────────────────────────────
    try:
        user_context = build_user_context(user_id) if user_id is not None else ""
    except Exception as exc:
        print(f"  [user_context] error: {exc}")
        user_context = ""

    # ── HISTORY PREFIX & OPENER VARIATION ─────────────────────────────────
    history_prefix, last_opener = format_history(history)

    # Combine history prefix + user context (if any) + current question
    question_with_context = ""
    if history_prefix:
        question_with_context += history_prefix
    if user_context:
        question_with_context += user_context + "\n\n"
    question_with_context += f"Current Message: {question}"

    # ── FORMAT PROMPT ─────────────────────────────────────────────────────
    prompt   = get_prompt(language)
    messages = prompt.format_messages(
        context=context,
        mental_state=mental_state,
        question=question_with_context,
    )

    # ── LLM GENERATION & POST-PROCESSING ──────────────────────────────────
    response_text, regenerated = _invoke_and_validate(messages, question, language)
    response_text = clean_user_response(response_text, language, context, question)

    # ── NATURAL JOURNAL CONTEXT INTEGRATION (Language-Aware & Varied) ─────
    journal_match = re.search(r"^\s*\d+\.\s*\[[^\]]+\]\s*(.+)$", user_context, re.MULTILINE)
    first_journal = journal_match.group(1).strip() if journal_match else ""
    if (
        first_journal
        and _journal_is_relevant(question, first_journal)
        and not _response_mentions_journal(response_text, first_journal)
    ):
        if language == "roman_urdu":
            journal_note = f"Aap ne apni journal mein likha tha: '{first_journal}' — is baat ka asar abhi tak hona bilkul samajh aata hai.\n\n"
        elif language == "urdu":
            journal_note = f"آپ نے اپنی ڈائری میں لکھا تھا: '{first_journal}' — اس کا اثر ابھی تک محسوس ہونا بالکل فطری ہے۔\n\n"
        else:
            journal_note = f"Earlier in your journal, you noted: '{first_journal}' — which connects closely with what you are experiencing now.\n\n"
        response_text = journal_note + response_text

    if regenerated:
        print("  Note: response was regenerated due to quality check.")
    print("Response generated successfully.")

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
    }


# =====================================================
# Helpers
# =====================================================

def get_retrieved_chunks(question: str) -> List[Document]:
    return retriever.invoke(question)
