# -*- coding: utf-8 -*-
"""Create reviewer worksheets from one complete raw JSONL run.

Run from backend: python -m app.ai.evaluation_rag_llm.prepare_review --raw ../VALIDATION/rag_llm/raw_run_....jsonl
Outputs enriched score/retrieval CSVs; refuses incomplete runs and never overwrites human annotations.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from app.ai.evaluation_rag_llm.evaluation_dataset import EVALUATION_DATASET
from app.ai.evaluation_rag_llm.evaluation_rubric import RUBRIC

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_DIR = ROOT / "VALIDATION" / "rag_llm"


def _load_run(path: Path) -> dict[str, dict]:
    cases = {}
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            case_id = row.get("test_id")
            if case_id in cases:
                raise ValueError(f"Duplicate test_id {case_id!r} in raw run.")
            if row.get("status") not in (None, "generated_unscored") or row.get("scored") is True:
                raise ValueError(f"{case_id}: raw case is not an unscored successful generation.")
            if not row.get("question") or not (row.get("display_response") or row.get("raw_response")):
                raise ValueError(f"{case_id}: missing question or generated response.")
            cases[case_id] = row
    expected = {item["test_id"] for item in EVALUATION_DATASET}
    if set(cases) != expected:
        raise ValueError(f"Expected exactly 30 successful cases; missing={sorted(expected-set(cases))}, extra={sorted(set(cases)-expected)}")
    return cases


def prepare(raw_path: Path, output_dir: Path, *, overwrite: bool = False) -> tuple[Path, Path]:
    cases = _load_run(raw_path)
    scores_path = output_dir / "scores.csv"
    retrieval_path = output_dir / "retrieval_metrics.csv"
    if not overwrite and (scores_path.exists() or retrieval_path.exists()):
        raise FileExistsError("Review worksheets already exist; refusing overwrite. Choose --output-dir or --overwrite only after backing up human annotations.")
    output_dir.mkdir(parents=True, exist_ok=True)
    score_fields = ["test_id", "reviewer_role", "question", "expected_behavior", "model_tag", "prompt_sha256", "retrieved_chunks_json", "system_answer", *[f"{name}_score_1_to_5" for name in RUBRIC], "comments", "scored"]
    retrieval_fields = ["test_id", "reviewer_role", "question", "retrieved_chunk_ids", "retrieved_chunks_json", "relevant_retrieved_chunk_ids", "all_relevant_chunk_ids", "precision_at_k", "coverage_recall", "comments"]
    dataset = {item["test_id"]: item for item in EVALUATION_DATASET}
    with scores_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=score_fields)
        writer.writeheader()
        for case_id in sorted(cases):
            run, specification = cases[case_id], dataset[case_id]
            for reviewer in ("reviewer_1", "reviewer_2"):
                writer.writerow({"test_id": case_id, "reviewer_role": reviewer,
                    "question": run["question"], "expected_behavior": run.get("expected_behavior", specification["expected_behavior"]),
                    "model_tag": run.get("model_tag", ""), "prompt_sha256": run.get("prompt_sha256", ""),
                    "retrieved_chunks_json": json.dumps(run.get("retrieved_chunks", []), ensure_ascii=False),
                    "system_answer": run.get("display_response") or run.get("raw_response", ""),
                    **{f"{name}_score_1_to_5": "" for name in RUBRIC}, "comments": "", "scored": "false"})
    with retrieval_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=retrieval_fields)
        writer.writeheader()
        for case_id in sorted(cases):
            run = cases[case_id]
            ids = run.get("retrieved_chunk_ids", [])
            chunks = run.get("retrieved_chunks", [])
            # Normalize legacy raw runs that recorded base IDs rather than occurrence IDs.
            if ids and not all("#" in value for value in ids):
                counts = {}
                normalized = []
                for value in ids:
                    counts[value] = counts.get(value, 0) + 1
                    normalized.append(f"{value}#{counts[value]}")
                ids = normalized
            for reviewer in ("reviewer_1", "reviewer_2"):
                writer.writerow({"test_id": case_id, "reviewer_role": reviewer,
                    "question": run["question"], "retrieved_chunk_ids": ";".join(ids),
                    "retrieved_chunks_json": json.dumps(chunks, ensure_ascii=False),
                    "relevant_retrieved_chunk_ids": "", "all_relevant_chunk_ids": "",
                    "precision_at_k": "", "coverage_recall": "", "comments": ""})
    return scores_path, retrieval_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True, help="A complete raw_run_*.jsonl")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace existing sheets; archive human work first")
    args = parser.parse_args()
    try:
        score, retrieval = prepare(args.raw, args.output_dir, overwrite=args.overwrite)
        print(f"Score sheet: {score}\nRetrieval sheet: {retrieval}")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"REVIEW PREPARATION REFUSED: {exc}") from exc
