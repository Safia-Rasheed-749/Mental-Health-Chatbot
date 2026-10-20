# -*- coding: utf-8 -*-
"""Run the 30-case local RAG evaluation without fabricating human scores.

Run from ``backend`` with ``python -m app.ai.evaluation_rag_llm.run_evaluation``.
The runner fails before inference if the configured Ollama model is unavailable.
Successful generations are saved as JSONL; scores remain explicitly unscored
until two reviewers complete the rubric.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from app.ai.evaluation_rag_llm.evaluation_dataset import EVALUATION_DATASET
from app.ai.evaluation_rag_llm.evaluation_rubric import RUBRIC
# Load backend .env before resolving the same model tag used by the service.
from app.core.config import settings as _settings  # noqa: F401
from app.ai.llm.llm import DEFAULT_MODEL_NAME

PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUTPUT = PROJECT_ROOT / "VALIDATION" / "rag_llm"
DIMENSIONS = tuple(RUBRIC)


def _ollama_base_url(value: str) -> str:
    value = value.strip()
    if "://" not in value:
        value = "http://" + value
    return value.rstrip("/")


def ollama_preflight(model_name: str, base_url: str, timeout: float = 5.0) -> dict:
    """Require Ollama and the exact requested model tag; return tag/digest."""
    url = _ollama_base_url(base_url) + "/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Ollama preflight failed at {url}: {exc}") from exc

    models = payload.get("models", [])
    model = next((item for item in models if item.get("name") == model_name), None)
    if model is None:
        installed = ", ".join(sorted(item.get("name", "?") for item in models)) or "none"
        raise RuntimeError(
            f"Configured Ollama model {model_name!r} is not installed. Installed tags: {installed}. "
            f"Install it with: ollama pull {model_name}"
        )
    return {"name": model_name, "digest": model.get("digest"), "ollama_url": _ollama_base_url(base_url)}


def _make_score_template(path: Path) -> None:
    if path.exists():
        return  # Never overwrite reviewers' work.
    fields = ["test_id", "reviewer_role", *[f"{name}_score_1_to_5" for name in DIMENSIONS], "comments", "scored"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in EVALUATION_DATASET:
            for reviewer in ("reviewer_1", "reviewer_2"):
                writer.writerow({
                    "test_id": item["test_id"],
                    "reviewer_role": reviewer,
                    **{f"{name}_score_1_to_5": "" for name in DIMENSIONS},
                    "comments": "",
                    "scored": "false",
                })


def _make_retrieval_template(path: Path, cases: list[dict]) -> None:
    if path.exists():
        return
    fields = [
        "test_id", "question", "retrieved_chunk_ids", "relevant_retrieved_chunk_ids",
        "all_relevant_chunk_ids", "precision_at_k", "coverage_recall", "reviewer_role", "comments",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for case in cases:
            retrieved_ids = case["retrieved_chunk_ids"]
            for reviewer in ("reviewer_1", "reviewer_2"):
                writer.writerow({
                    "test_id": case["test_id"],
                    "question": case["question"],
                    "retrieved_chunk_ids": ";".join(retrieved_ids),
                    "relevant_retrieved_chunk_ids": "",
                    "all_relevant_chunk_ids": "",
                    "precision_at_k": "",
                    "coverage_recall": "",
                    "reviewer_role": reviewer,
                    "comments": "",
                })


def _occurrence_ids(chunk_ids: list[str]) -> list[str]:
    """Give repeated identical chunks distinct, annotatable retrieval IDs."""
    counts: dict[str, int] = {}
    output = []
    for chunk_id in chunk_ids:
        counts[chunk_id] = counts.get(chunk_id, 0) + 1
        output.append(f"{chunk_id}#{counts[chunk_id]}")
    return output


def run(model_name: str | None = None, ollama_url: str | None = None) -> Path:
    model_name = model_name or os.getenv("OLLAMA_MODEL", DEFAULT_MODEL_NAME)
    ollama_url = ollama_url or os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    model = ollama_preflight(model_name, ollama_url)

    # Import only after preflight: rag_chat_service eagerly loads FAISS, embedding,
    # classifiers and the local LLM at module import time.
    from app.services.rag_chat_service import generate_response_with_context

    OUTPUT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    raw_path = OUTPUT / f"raw_run_{timestamp}.jsonl"
    metadata_path = OUTPUT / f"run_{timestamp}.metadata.json"
    run_metadata = {
        "status": "running",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "model": model,
        "cases_expected": len(EVALUATION_DATASET),
        "cases_completed": 0,
        "scoring": "not_scored; human rubric required",
        "rubric_dimensions": list(DIMENSIONS),
        "evaluation_dataset_sha256": hashlib.sha256(
            json.dumps(EVALUATION_DATASET, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest(),
    }
    completed = []
    failure = None

    with raw_path.open("w", encoding="utf-8") as handle:
        for item in EVALUATION_DATASET:
            started = perf_counter()
            try:
                result = generate_response_with_context(item["user_question"])
                latency = perf_counter() - started
                chunks = result.get("retrieved_chunks", [])
                row = {
                    "test_id": item["test_id"],
                    "category": item["category"],
                    "question": item["user_question"],
                    "expected_behavior": item["expected_behavior"],
                    "model_tag": model["name"],
                    "model_digest": model.get("digest"),
                    "prompt_sha256": result.get("prompt_sha256"),
                    "latency_seconds": round(latency, 4),
                    "retrieved_chunk_ids": _occurrence_ids([chunk["chunk_id"] for chunk in chunks]),
                    "retrieved_chunks": chunks,
                    "retrieved_context": result.get("context", ""),
                    "raw_response": result.get("raw_response", ""),
                    "display_response": result.get("response", ""),
                    "scored": False,
                    "status": "generated_unscored",
                }
                completed.append(row)
            except Exception as exc:
                latency = perf_counter() - started
                row = {
                    "test_id": item["test_id"],
                    "category": item["category"],
                    "question": item["user_question"],
                    "model_tag": model["name"],
                    "model_digest": model.get("digest"),
                    "latency_seconds": round(latency, 4),
                    "scored": False,
                    "status": "generation_error",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
                failure = f"{item['test_id']}: {type(exc).__name__}: {exc}"
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            if failure:
                break

    run_metadata["cases_completed"] = len(completed)
    run_metadata["raw_jsonl"] = raw_path.name
    run_metadata["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    run_metadata["status"] = "incomplete" if failure else "generated_unscored"
    if failure:
        run_metadata["failure"] = failure
    metadata_path.write_text(json.dumps(run_metadata, indent=2), encoding="utf-8")

    if failure:
        raise RuntimeError(f"Evaluation stopped and is marked incomplete ({failure}). Raw partial run: {raw_path}")
    if len(completed) != len(EVALUATION_DATASET):
        raise RuntimeError(f"Expected {len(EVALUATION_DATASET)} cases, got {len(completed)}; no score template created.")

    _make_score_template(OUTPUT / "scores.csv")
    _make_retrieval_template(OUTPUT / "retrieval_metrics.csv", completed)
    print(f"Generated {len(completed)} cases; they remain unscored. Raw run: {raw_path}")
    print(f"Two reviewers must complete {OUTPUT / 'scores.csv'} before a summary can be produced.")
    return raw_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=None, help="Ollama model tag (defaults to OLLAMA_MODEL/configured default)")
    parser.add_argument("--ollama-url", default=None, help="Ollama base URL; defaults to OLLAMA_HOST or localhost:11434")
    args = parser.parse_args()
    try:
        run(args.model, args.ollama_url)
    except Exception as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
