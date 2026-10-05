"""
=========================================================
Evaluation Runner
Project : AI Mental Health Chatbot (FYP)

Runs all 30 evaluation questions through the existing
RAG + llama3.2:1b pipeline and saves raw results as JSON.

What this script does
---------------------
1. Loads all 30 questions from EVALUATION_DATASET.
2. Loads the existing FAISS vector store (never rebuilds it).
3. Retrieves top-4 chunks for every question.
4. Sends each question + context to local llama3.2:1b via ChatOllama.
5. Saves per-question results including:
      - test_id, category, user_question
      - expected_behavior
      - retrieved_chunks  (list of dicts with content + source metadata)
      - generated_response
      - blank scoring fields for manual evaluation:
            context_relevance_score   (null — fill manually)
            faithfulness_score        (null — fill manually)
            response_relevance_score  (null — fill manually)
            safety_score              (null — fill manually)
            helpfulness_score         (null — fill manually)
            evaluator_comments        ("" — fill manually)
6. Writes the full results list to JSON in:
      backend/app/ai/evaluation_rag_llm/results/

What this script does NOT do
-----------------------------
- It does NOT assign scores automatically.
- It does NOT modify the vector store or embeddings.
- It does NOT modify evaluation_dataset.py or evaluation_rubric.py.
- It does NOT rebuild the FAISS index.

Configurable
------------
MODEL_NAME  — swap to any Ollama model for comparison runs.
TOP_K       — number of retrieved chunks (default: 4).

Run from the backend/ directory:
    python -m app.ai.evaluation_rag_llm.run_evaluation
=========================================================
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Reuse existing RAG + LLM components ──────────────────
from ..rag.embeddings import get_embedding_model
from ..rag.vector_store import load_vector_store
from ..rag.retriever import get_retriever
from ..llm.llm import get_llm
from ..llm.prompt import get_prompt

# ── Evaluation dataset (unchanged) ───────────────────────
from .evaluation_dataset import EVALUATION_DATASET

# ─────────────────────────────────────────────────────────
# Configuration — change MODEL_NAME here to compare models
# ─────────────────────────────────────────────────────────
MODEL_NAME  = "llama3.2:1b"
TOP_K       = 4

# Output directory — relative to this file
RESULTS_DIR = Path(__file__).parent / "results"


# =====================================================
# Initialise RAG + LLM stack
# =====================================================

def initialise():
    """
    Load all components needed for the evaluation run.

    Reuses the same initialisation pattern as test_rag_llm.py.

    Returns:
        (retriever, llm, prompt) tuple.
    """
    print("\n" + "=" * 60)
    print("EVALUATION RUNNER — AI Mental Health Chatbot FYP")
    print("=" * 60)
    print(f"Model            : {MODEL_NAME}")
    print(f"Top-K retrieval  : {TOP_K}")
    print(f"Questions total  : {len(EVALUATION_DATASET)}")
    print("=" * 60)

    print("\n[1/4] Loading embedding model ...")
    embeddings = get_embedding_model()

    print("[2/4] Loading existing FAISS vector store ...")
    vector_store = load_vector_store(embeddings)

    print("[3/4] Building retriever ...")
    retriever = get_retriever(
        vector_store=vector_store,
        search_kwargs={"k": TOP_K},
    )

    print(f"[4/4] Creating LLM ({MODEL_NAME}) ...")
    llm = get_llm(model_name=MODEL_NAME)

    prompt = get_prompt()

    print("\nAll components loaded successfully.\n")
    return retriever, llm, prompt


# =====================================================
# Build context string from retrieved documents
# =====================================================

def build_context(documents: list) -> str:
    """
    Combine retrieved document chunks into a single context string.
    Identical to the helper in test_rag_llm.py.
    """
    parts = []
    for idx, doc in enumerate(documents, start=1):
        parts.append(f"[Chunk {idx}]\n{doc.page_content}")
    return "\n\n".join(parts)


# =====================================================
# Serialise retrieved documents for JSON storage
# =====================================================

def serialise_chunks(documents: list) -> list:
    """
    Convert LangChain Document objects to plain dicts for JSON.

    Each dict contains:
        chunk_index : 1-based index
        content     : page content
        source      : filename from metadata (if available)
        page        : page number from metadata (if available)
    """
    chunks = []
    for idx, doc in enumerate(documents, start=1):
        meta   = doc.metadata or {}
        source = meta.get("source", "unknown")
        page   = meta.get("page", None)
        chunks.append({
            "chunk_index": idx,
            "content":     doc.page_content,
            "source":      str(source),
            "page":        page,
        })
    return chunks


# =====================================================
# Run a single question through the pipeline
# =====================================================

def run_one(question_data: dict, retriever, llm, prompt) -> dict:
    """
    Run one evaluation question through the RAG + LLM pipeline.

    Args:
        question_data : dict from EVALUATION_DATASET
        retriever     : FAISS retriever (k=4)
        llm           : ChatOllama instance
        prompt        : ChatPromptTemplate

    Returns:
        Result dict with raw outputs and blank scoring fields.
    """
    test_id   = question_data["test_id"]
    category  = question_data["category"]
    question  = question_data["user_question"]
    expected  = question_data["expected_behavior"]
    focus     = question_data["evaluation_focus"]

    print(f"  [{test_id}] {question[:70]}{'...' if len(question) > 70 else ''}")

    # ── Retrieval ────────────────────────────────────────
    try:
        documents = retriever.invoke(question)
    except Exception as exc:
        print(f"    [ERROR] Retrieval failed: {exc}")
        documents = []

    retrieved_chunks = serialise_chunks(documents)

    # ── Generation ───────────────────────────────────────
    generated_response = ""

    if not documents:
        generated_response = "[ERROR] No documents retrieved — response not generated."
    else:
        context = build_context(documents)
        try:
            messages  = prompt.format_messages(context=context, question=question)
            response  = llm.invoke(messages)
            generated_response = (
                response.content if hasattr(response, "content") else str(response)
            )
        except Exception as exc:
            generated_response = f"[ERROR] LLM invocation failed: {exc}"

    # ── Result record (blank scores for manual evaluation) ──
    return {
        "test_id":                    test_id,
        "category":                   category,
        "user_question":              question,
        "evaluation_focus":           focus,
        "expected_behavior":          expected,
        "retrieved_chunks":           retrieved_chunks,
        "generated_response":         generated_response,
        # ── BLANK fields — fill these manually using the rubric ──
        "context_relevance_score":    None,
        "faithfulness_score":         None,
        "response_relevance_score":   None,
        "safety_score":               None,
        "helpfulness_score":          None,
        "per_question_average":       None,
        "evaluator_comments":         "",
    }


# =====================================================
# Save results to JSON
# =====================================================

def save_results(results: list, model_name: str) -> Path:
    """
    Save the evaluation results list to a JSON file.

    Filename format:
        eval_results_<model>_<YYYYMMDD_HHMMSS>.json

    Args:
        results    : list of result dicts (one per question)
        model_name : model identifier string

    Returns:
        Path to the saved file.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Sanitise model name for filename
    safe_model = model_name.replace(":", "_").replace("/", "_")
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename   = f"eval_results_{safe_model}_{timestamp}.json"
    filepath   = RESULTS_DIR / filename

    output = {
        "metadata": {
            "project":        "AI Mental Health Chatbot — FYP",
            "model":          model_name,
            "top_k":          TOP_K,
            "total_questions": len(results),
            "run_timestamp":  datetime.now().isoformat(),
            "scoring_status": (
                "BLANK — scores must be filled manually using evaluation_rubric.py"
            ),
            "dimensions": [
                "context_relevance_score",
                "faithfulness_score",
                "response_relevance_score",
                "safety_score",
                "helpfulness_score",
            ],
            "score_range":    "1 (worst) to 5 (best) per dimension",
            "max_per_question": 25,
            "instructions": (
                "For each result, read user_question, retrieved_chunks, "
                "generated_response, and expected_behavior. "
                "Apply the rubric in evaluation_rubric.py. "
                "Fill in each *_score field with an integer 1–5. "
                "Add your reasoning to evaluator_comments. "
                "Then calculate per_question_average = sum of 5 scores / 5."
            ),
        },
        "results": results,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return filepath


# =====================================================
# Main Entry Point
# =====================================================

def main() -> None:
    """
    Orchestrate the full evaluation run.

    Steps:
        1. Parse --limit argument (optional).
        2. Initialise RAG + LLM components.
        3. Run questions one by one (all 30 or limited subset).
        4. Save raw results with blank scoring fields.
        5. Print a summary.
    """

    # ── Parse command-line arguments ─────────────────────
    parser = argparse.ArgumentParser(
        description="Run RAG + LLM evaluation for AI Mental Health Chatbot FYP."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Number of questions to run (default: all 30). Example: --limit 3",
    )
    args = parser.parse_args()

    # Slice dataset if --limit provided
    dataset = EVALUATION_DATASET
    if args.limit is not None:
        if args.limit < 1:
            print("[ERROR] --limit must be a positive integer.")
            sys.exit(1)
        dataset = EVALUATION_DATASET[: args.limit]

    # ── Initialise ───────────────────────────────────────
    try:
        retriever, llm, prompt = initialise()
    except FileNotFoundError as exc:
        print(f"\n[ERROR] {exc}")
        print("The FAISS vector store is missing.")
        print("Run the RAG pipeline first:  python -m app.ai.rag.pipeline")
        sys.exit(1)
    except ConnectionError as exc:
        print(f"\n[ERROR] Cannot reach Ollama: {exc}")
        print("Start Ollama and ensure llama3.2:1b is pulled.")
        sys.exit(1)
    except Exception as exc:
        err = str(exc)
        if "not found" in err.lower() or "pull" in err.lower():
            print(f"\n[ERROR] Model not available: {exc}")
            print(f"Pull it with:  ollama pull {MODEL_NAME}")
        else:
            print(f"\n[ERROR] Initialisation failed: {exc}")
        sys.exit(1)

    # ── Run all questions ─────────────────────────────────
    print(f"Running {len(dataset)} evaluation questions ...\n")
    results = []

    for idx, question_data in enumerate(dataset, start=1):
        print(f"Question {idx:02d}/{len(dataset)}", end=" ")
        result = run_one(question_data, retriever, llm, prompt)
        results.append(result)

    # ── Save results ─────────────────────────────────────
    print(f"\n{'=' * 60}")
    print("Saving evaluation results ...")
    filepath = save_results(results, MODEL_NAME)

    # ── Summary ──────────────────────────────────────────
    print(f"\n{'=' * 60}")
    print("EVALUATION RUN COMPLETE")
    print(f"{'=' * 60}")
    print(f"Questions run    : {len(results)}")
    print(f"Model used       : {MODEL_NAME}")
    print(f"Results saved to : {filepath}")
    print(f"{'=' * 60}")
    print()
    print("NEXT STEP — Manual Scoring:")
    print("  1. Open the JSON file above.")
    print("  2. For each result, read: user_question, retrieved_chunks,")
    print("     generated_response, and expected_behavior.")
    print("  3. Open evaluation_rubric.py and apply the 5-dimension rubric.")
    print("  4. Fill in: context_relevance_score, faithfulness_score,")
    print("     response_relevance_score, safety_score, helpfulness_score")
    print("     (integers 1–5 each).")
    print("  5. Add your reasoning to evaluator_comments.")
    print("  6. Calculate per_question_average = sum of 5 scores / 5.")
    print("  7. After all 30 are scored, calculate column averages")
    print("     and the overall average.")
    print()
    print("To run the same evaluation with a different model:")
    print("  Change MODEL_NAME at the top of run_evaluation.py")
    print("  and run again. Results will be saved as a separate file.")
    print(f"{'=' * 60}")


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":
    main()
