"""Run the curated RAG evaluation set and export an examiner-ready dataset.

This runner deliberately does not invent automated clinical scores. It records
the question, retrieved chunks, model response, and expected behaviour so the
five dimensions in ``evaluation_rubric.py`` can be scored transparently by a
reviewer. Optional automatic metrics can be added later without changing the
dataset format.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from app.ai.evaluation_rag_llm.evaluation_dataset import EVALUATION_DATASET
from app.services.rag_chat_service import generate_response_with_context

OUTPUT = Path(__file__).resolve().parents[3] / "evaluation" / "rag_llm"


def run() -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in EVALUATION_DATASET:
        result = generate_response_with_context(item["user_question"])
        rows.append({
            "test_id": item["test_id"],
            "category": item["category"],
            "question": item["user_question"],
            "expected_behavior": item["expected_behavior"],
            "response": result["response"],
            "retrieved_context": result["context"],
            "context_relevance_score_1_to_5": "",
            "faithfulness_score_1_to_5": "",
            "response_relevance_score_1_to_5": "",
            "safety_score_1_to_5": "",
            "helpfulness_score_1_to_5": "",
            "reviewer_comments": "",
        })
    output_file = OUTPUT / "rag_evaluation_results.csv"
    with output_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    (OUTPUT / "rag_evaluation_metadata.json").write_text(
        json.dumps({"samples": len(rows), "scores": "manual rubric required"}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} evaluation cases to {output_file}")
    return output_file


if __name__ == "__main__":
    run()
