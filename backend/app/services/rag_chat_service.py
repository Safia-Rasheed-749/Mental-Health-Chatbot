# backend/app/services/rag_chat_service.py

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
        -> format prompt  (context + mental_state + question)
        -> LLM generates response
        -> return response text + raw detection results
"""

from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_core.documents import Document

from app.ai.emotion_detection.predict import predict_emotion
from app.ai.stress_detection.predict import predict_stress
from app.ai.depression_detection.predict import predict_depression

from app.ai.llm.llm import get_llm
from app.ai.llm.prompt import get_prompt, detect_language
from app.ai.rag.embeddings import get_embedding_model
from app.ai.rag.retriever import get_retriever
from app.ai.rag.vector_store import load_vector_store

# =====================================================
# Configuration
# =====================================================

TOP_K = 4          # Number of RAG chunks to retrieve
LOW_CONF = 60.0    # Confidence threshold below which a label is "unreliable"

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
# Run All Detectors
# =====================================================

def run_detectors(text: str) -> Tuple[dict, dict, dict]:
    """
    Run all three mental-health classifiers on the user's message.

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


# Initialize once when the module is first imported.
# All subsequent requests reuse the same warm instances.
retriever, llm = initialize_rag_chat()


# =====================================================
# Main Chat Function
# =====================================================

def generate_chat_response(question: str) -> dict:
    """
    Generate a response using detectors + RAG + LLM.

    Full pipeline:
        1. Run emotion / stress / depression classifiers
        2. Retrieve relevant chunks from FAISS
        3. Build mental_state string from classifier outputs
        4. Build context string from retrieved chunks
        5. Format prompt  (context + mental_state + question)
        6. Generate LLM response
        7. Return response text together with raw detection scores

    Args:
        question: User's message.

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

    # --------------------------------------------------
    # Step 1: Detect language (Python-side — reliable)
    # --------------------------------------------------
    language = detect_language(question)
    print(f"  Detected language: {language}")

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
            "emotion":               emotion_result["emotion"],
            "emotion_confidence":    emotion_result["confidence"],
            "stress":                stress_result["stress"],
            "stress_confidence":     stress_result["confidence"],
            "depression":            depression_result["depression"],
            "depression_confidence": depression_result["confidence"],
        }

    # --------------------------------------------------
    # Step 4: Build context and mental_state strings
    # --------------------------------------------------
    context      = build_context(documents)
    mental_state = build_mental_state(emotion_result, stress_result, depression_result)

    # --------------------------------------------------
    # Step 5: Select language-specific prompt and format
    # --------------------------------------------------
    prompt = get_prompt(language)
    messages = prompt.format_messages(
        context=context,
        mental_state=mental_state,
        question=question,
    )

    # --------------------------------------------------
    # Step 6: Generate LLM response
    # --------------------------------------------------
    raw_response  = llm.invoke(messages)
    response_text = (
        raw_response.content
        if hasattr(raw_response, "content")
        else str(raw_response)
    )

    print("Response generated successfully.")

    # --------------------------------------------------
    # Step 7: Return enriched result
    # --------------------------------------------------
    return {
        "response":              response_text,
        "emotion":               emotion_result["emotion"],
        "emotion_confidence":    emotion_result["confidence"],
        "stress":                stress_result["stress"],
        "stress_confidence":     stress_result["confidence"],
        "depression":            depression_result["depression"],
        "depression_confidence": depression_result["confidence"],
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
    )

    raw_response  = llm.invoke(messages)
    response_text = (
        raw_response.content
        if hasattr(raw_response, "content")
        else str(raw_response)
    )

    return {
        "question":         question,
        "response":         response_text,
        "context":          context,
        "mental_state":     mental_state,
        "retrieved_chunks": documents,
        "emotion_result":   emotion_result,
        "stress_result":    stress_result,
        "depression_result": depression_result,
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
