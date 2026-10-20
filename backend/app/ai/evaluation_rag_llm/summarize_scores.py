# -*- coding: utf-8 -*-
"""Validate two-reviewer score sheets and write summary only when complete."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

from app.ai.evaluation_rag_llm.evaluation_dataset import EVALUATION_DATASET
from app.ai.evaluation_rag_llm.evaluation_rubric import RUBRIC

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = PROJECT_ROOT / "VALIDATION" / "rag_llm" / "scores.csv"
DIMENSIONS = tuple(RUBRIC)


def _cohen_kappa(left: list[int], right: list[int]) -> float:
    n = len(left)
    if not n:
        raise ValueError("Cohen's kappa needs at least one paired rating.")
    observed = sum(a == b for a, b in zip(left, right)) / n
    categories = range(1, 6)
    left_counts = {value: left.count(value) / n for value in categories}
    right_counts = {value: right.count(value) / n for value in categories}
    expected = sum(left_counts[value] * right_counts[value] for value in categories)
    if math.isclose(expected, 1.0):
        return 1.0 if math.isclose(observed, 1.0) else 0.0
    return (observed - expected) / (1.0 - expected)


def summarize(scores_path: Path, report_path: Path) -> Path:
    expected_ids = {item["test_id"] for item in EVALUATION_DATASET}
    required_reviewers = {"reviewer_1", "reviewer_2"}
    rating_columns = {dimension: f"{dimension}_score_1_to_5" for dimension in DIMENSIONS}
    rows = list(csv.DictReader(scores_path.open(encoding="utf-8-sig", newline="")))
    if not rows:
        raise ValueError("Score sheet is empty.")

    by_case_reviewer: dict[tuple[str, str], dict] = {}
    for row_number, row in enumerate(rows, start=2):
        test_id = (row.get("test_id") or "").strip()
        reviewer = (row.get("reviewer_role") or "").strip()
        if test_id not in expected_ids:
            raise ValueError(f"Row {row_number}: unexpected test_id {test_id!r}.")
        if reviewer not in required_reviewers:
            raise ValueError(f"Row {row_number}: reviewer_role must be reviewer_1 or reviewer_2.")
        key = (test_id, reviewer)
        if key in by_case_reviewer:
            raise ValueError(f"Duplicate score row for {key}.")
        parsed = {}
        for dimension, column in rating_columns.items():
            value = (row.get(column) or "").strip()
            if not value:
                raise ValueError(f"Row {row_number}: missing {column}; summary refused.")
            try:
                score = int(value)
            except ValueError as exc:
                raise ValueError(f"Row {row_number}: {column} must be an integer 1–5.") from exc
            if score not in range(1, 6):
                raise ValueError(f"Row {row_number}: {column} must be an integer 1–5.")
            parsed[dimension] = score
        by_case_reviewer[key] = parsed

    expected_pairs = {(case_id, reviewer) for case_id in expected_ids for reviewer in required_reviewers}
    missing = expected_pairs - set(by_case_reviewer)
    extra = set(by_case_reviewer) - expected_pairs
    if missing or extra:
        raise ValueError(f"Expected 30 cases × 2 reviewers; missing={len(missing)}, extra={len(extra)}.")

    lines = [
        "# Human-scored RAG/LLM evaluation",
        "",
        f"- Cases scored: {len(expected_ids)}/{len(expected_ids)}",
        "- Reviewers: two anonymous reviewer roles (`reviewer_1`, `reviewer_2`)",
        "- Scale: 1–5; see `backend/app/ai/evaluation_rag_llm/evaluation_rubric.py` for anchors.",
        "- This is a human evaluation of this run only, not clinical validation.",
        "",
        "| Dimension | Mean | Sample SD | Cohen's κ | Exact agreement |",
        "|---|---:|---:|---:|---:|",
    ]
    for dimension in DIMENSIONS:
        left = [by_case_reviewer[(case_id, "reviewer_1")][dimension] for case_id in sorted(expected_ids)]
        right = [by_case_reviewer[(case_id, "reviewer_2")][dimension] for case_id in sorted(expected_ids)]
        pooled = left + right
        mean = sum(pooled) / len(pooled)
        sd = math.sqrt(sum((value - mean) ** 2 for value in pooled) / (len(pooled) - 1))
        agreement = sum(a == b for a, b in zip(left, right)) / len(left)
        kappa = _cohen_kappa(left, right)
        lines.append(f"| {dimension.replace('_', ' ').title()} | {mean:.2f} | {sd:.2f} | {kappa:.3f} | {agreement:.1%} |")
    lines.extend([
        "",
        "## Case diagnostics",
        "",
        "Case means below 3.0 are flagged for human review; this threshold is a diagnostic convention, not a pass/fail safety guarantee.",
        "",
        "| Case | Reviewer | Dimension means | Low scores (<3) | Comments |",
        "|---|---|---|---|---|",
    ])
    for case_id in sorted(expected_ids):
        for reviewer in sorted(required_reviewers):
            ratings = by_case_reviewer[(case_id, reviewer)]
            low = [name for name, value in ratings.items() if value < 3]
            original = next(row for row in rows if row["test_id"].strip() == case_id and row["reviewer_role"].strip() == reviewer)
            comments = (original.get("comments") or "").replace("|", "\\|").replace("\n", " ")
            means = ", ".join(f"{name.replace('_', ' ')}={value}" for name, value in ratings.items())
            lines.append(f"| {case_id} | {reviewer} | {means} | {', '.join(low) or 'none'} | {comments} |")
    lines.extend([
        "",
        "## Interpretation and limitations",
        "",
        "Cohen's κ is unweighted and computed per rubric dimension across the 30 paired ratings. "
        "It is descriptive; it does not prove answer quality, safety, or clinical effectiveness. "
        "Include reviewed failure examples and model/prompt hashes before making any quality claim.",
        "",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_INPUT.with_name("REPORT.md"))
    arguments = parser.parse_args()
    try:
        print(summarize(arguments.scores, arguments.report))
    except (OSError, ValueError) as error:
        raise SystemExit(f"SUMMARY REFUSED: {error}") from error
