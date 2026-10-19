# -*- coding: utf-8 -*-
"""Run the curated crisis detector matrix and save honest diagnostic metrics."""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
from app.services.crisis_detector import detect_crisis

CASES_PATH = ROOT / "backend" / "tests" / "safety" / "crisis_matrix.json"
OUT = ROOT / "VALIDATION" / "safety"


def run() -> tuple[Path, Path]:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    rows = []
    tp = fp = tn = fn = 0
    for case in cases:
        predicted = bool(detect_crisis(case["text"])["is_crisis"])
        expected = bool(case["expected_crisis"])
        tp += expected and predicted
        fn += expected and not predicted
        fp += not expected and predicted
        tn += not expected and not predicted
        rows.append({**case, "predicted_crisis": predicted, "correct": predicted == expected})
    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "crisis_matrix_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cases": len(rows),
        "true_positive": int(tp), "false_positive": int(fp),
        "true_negative": int(tn), "false_negative": int(fn),
        "precision": precision, "recall": recall,
        "scope": "small, hand-authored regression matrix; not comprehensive validation",
        "missed_cases": [row["id"] for row in rows if row["expected_crisis"] and not row["predicted_crisis"]],
        "false_trigger_cases": [row["id"] for row in rows if not row["expected_crisis"] and row["predicted_crisis"]],
    }
    json_path = OUT / "crisis_matrix_metrics.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = [
        "# Crisis phrase-matrix diagnostic (not comprehensive)", "",
        f"Generated: {report['generated_at_utc']}", "",
        f"Cases: {len(rows)}; TP={tp}, FP={fp}, TN={tn}, FN={fn}; precision={precision:.3f}; recall={recall:.3f}.", "",
        "This is a small, hand-authored test set, not a representative sample and not proof of crisis coverage. Phrase matching can miss novel/indirect expressions and may false-trigger. The tool is not emergency monitoring or a hotline.", "",
        f"Missed positive cases: {', '.join(report['missed_cases']) or 'none in this small matrix'}.",
        f"False triggers: {', '.join(report['false_trigger_cases']) or 'none in this small matrix'}.", "",
        "See `crisis_matrix_results.csv` for each labeled input and output.", "",
    ]
    md_path = OUT / "CRISIS_MATRIX_REPORT.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    return csv_path, md_path


if __name__ == "__main__":
    for output in run():
        print(output)
