# -*- coding: utf-8 -*-
"""Score the curated crisis diagnostic matrix; reports are diagnostic, not coverage proof."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.crisis_detector import detect_crisis

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MATRIX = ROOT / "backend" / "tests" / "safety" / "crisis_matrix.json"
DEFAULT_REPORT = ROOT / "VALIDATION" / "safety" / "crisis_matrix_report.json"


def evaluate(matrix_path: Path) -> dict:
    cases = json.loads(matrix_path.read_text(encoding="utf-8"))
    ids = [case.get("id") for case in cases]
    if not cases or len(set(ids)) != len(ids):
        raise ValueError("Matrix must contain non-empty cases with unique IDs")
    tp = fp = fn = tn = 0
    details = []
    by_category = {}
    for case in cases:
        expected = bool(case["expected_crisis"])
        detected = bool(detect_crisis(case["text"])["is_crisis"])
        tp += expected and detected
        fn += expected and not detected
        fp += not expected and detected
        tn += not expected and not detected
        category = by_category.setdefault(case["category"], {"cases": 0, "correct": 0, "false_positive": 0, "false_negative": 0})
        category["cases"] += 1
        category["correct"] += expected == detected
        category["false_positive"] += not expected and detected
        category["false_negative"] += expected and not detected
        if expected != detected:
            details.append({"id": case["id"], "category": case["category"], "expected_crisis": expected, "detected_crisis": detected})
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {"case_count": len(cases), "confusion": {"true_positive": tp, "false_positive": fp, "false_negative": fn, "true_negative": tn},
            "precision": precision, "recall": recall, "accuracy": (tp + tn) / len(cases),
            "category_diagnostics": by_category, "misclassified_cases": details,
            "limitation": "Curated phrase matrix is a small diagnostic set, not comprehensive crisis detection or clinical validation."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    try:
        result = evaluate(args.matrix)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
    except (OSError, KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"CRISIS EVALUATION FAILED: {exc}") from exc
