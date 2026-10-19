# -*- coding: utf-8 -*-
"""Compute retrieval precision@k and recall only from complete manual labels."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

from app.ai.evaluation_rag_llm.evaluation_dataset import EVALUATION_DATASET

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = PROJECT_ROOT / "VALIDATION" / "rag_llm" / "retrieval_metrics.csv"


def _ids(value: str) -> set[str]:
    return {item.strip() for item in (value or "").split(";") if item.strip()}


def summarize(path: Path, report_path: Path, scored_path: Path) -> Path:
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig", newline="")))
    expected_ids = {item["test_id"] for item in EVALUATION_DATASET}
    pair_map = {}
    for number, row in enumerate(rows, start=2):
        key = (row.get("test_id", "").strip(), row.get("reviewer_role", "").strip())
        if key[0] not in expected_ids or key[1] not in {"reviewer_1", "reviewer_2"}:
            raise ValueError(f"Row {number}: unexpected case or reviewer.")
        if key in pair_map:
            raise ValueError(f"Row {number}: duplicate case/reviewer pair {key}.")
        retrieved = _ids(row.get("retrieved_chunk_ids", ""))
        relevant_retrieved = _ids(row.get("relevant_retrieved_chunk_ids", ""))
        all_relevant = _ids(row.get("all_relevant_chunk_ids", ""))
        if not relevant_retrieved or not all_relevant:
            raise ValueError(f"Row {number}: manual relevant-retrieved and all-relevant chunk IDs are required.")
        if not relevant_retrieved <= retrieved:
            raise ValueError(f"Row {number}: relevant retrieved IDs must be a subset of retrieved IDs.")
        if not relevant_retrieved <= all_relevant:
            raise ValueError(f"Row {number}: all relevant IDs must include relevant retrieved IDs.")
        if not retrieved:
            precision = 0.0
        else:
            precision = len(relevant_retrieved) / len(retrieved)
        recall = len(relevant_retrieved) / len(all_relevant)
        row["precision_at_k"] = f"{precision:.6f}"
        row["coverage_recall"] = f"{recall:.6f}"
        pair_map[key] = row
    expected_pairs = {(test_id, reviewer) for test_id in expected_ids for reviewer in ("reviewer_1", "reviewer_2")}
    if set(pair_map) != expected_pairs:
        raise ValueError(f"Expected 30 cases × 2 reviewers; have {len(pair_map)} labeled rows.")

    fields = list(rows[0])
    scored_path.parent.mkdir(parents=True, exist_ok=True)
    with scored_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(pair_map.values())
    precisions = [float(row["precision_at_k"]) for row in pair_map.values()]
    recalls = [float(row["coverage_recall"]) for row in pair_map.values()]
    mean_p = sum(precisions) / len(precisions)
    mean_r = sum(recalls) / len(recalls)
    sd_p = math.sqrt(sum((x - mean_p) ** 2 for x in precisions) / (len(precisions) - 1))
    sd_r = math.sqrt(sum((x - mean_r) ** 2 for x in recalls) / (len(recalls) - 1))
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "# Manual retrieval evaluation\n\n"
        f"- Paired annotations: {len(pair_map)} (30 questions × 2 reviewer roles)\n"
        f"- Mean precision@k: {mean_p:.3f} (sample SD {sd_p:.3f})\n"
        f"- Mean coverage/recall: {mean_r:.3f} (sample SD {sd_r:.3f})\n\n"
        "Metrics depend on reviewers' manually identified complete relevant-chunk sets; incomplete sheets are rejected. "
        "These results describe only this query set and index snapshot, not general retrieval quality. Review disagreements and source duplicates separately.\n",
        encoding="utf-8",
    )
    return report_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_INPUT.with_name("RETRIEVAL_REPORT.md"))
    parser.add_argument("--scored-output", type=Path, default=DEFAULT_INPUT.with_name("retrieval_metrics_scored.csv"))
    args = parser.parse_args()
    try:
        print(summarize(args.input, args.report, args.scored_output))
    except (OSError, ValueError) as error:
        raise SystemExit(f"RETRIEVAL SUMMARY REFUSED: {error}") from error
