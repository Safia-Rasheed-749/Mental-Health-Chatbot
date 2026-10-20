# -*- coding: utf-8 -*-
"""Recalculate held-out metrics and bootstrap CIs from saved predictions.

This consumes existing prediction CSVs only; it does not load or retrain models.
Stress error examples contain only labels/confidence and redacted text excerpts.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPECS = {
    "depression_deberta": ("backend/evaluation/depression_three_model_comparison/results/deberta_v3_base_test_predictions.csv", "backend/datasets/depression_v2/processed/test.csv"),
    "stress_deberta": ("backend/evaluation/stress_three_model_comparison/results/deberta_v3_base_test_predictions.csv", "backend/datasets/stress/processed/clean_test.csv"),
    "stress_roberta": ("backend/evaluation/stress_three_model_comparison/results/roberta_base_test_predictions.csv", "backend/datasets/stress/processed/clean_test.csv"),
}


def _read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    value = re.sub(r"https?://\S+|www\.\S+", " URLTOKEN ", value)
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    labels = sorted(set(y_true.tolist()) | set(y_pred.tolist()))
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    return {
        "sample_count": int(len(y_true)),
        "labels": labels,
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "confusion_matrix_labels_order": labels,
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
        "per_class": {str(label): {"precision": float(p), "recall": float(r), "f1": float(f), "support": int(s)}
                      for label, p, r, f, s in zip(labels, precision, recall, f1, support)},
    }


def bootstrap_ci(y_true: np.ndarray, y_pred: np.ndarray, seed: int = 42, replicates: int = 5000) -> dict:
    rng = np.random.default_rng(seed)
    scores = np.empty((replicates, 2), dtype=float)
    for i in range(replicates):
        idx = rng.integers(0, len(y_true), len(y_true))
        scores[i, 0] = accuracy_score(y_true[idx], y_pred[idx])
        scores[i, 1] = precision_recall_fscore_support(y_true[idx], y_pred[idx], average="macro", zero_division=0)[2]
    low, high = np.quantile(scores, [0.025, 0.975], axis=0)
    return {"method": "non-stratified percentile bootstrap over held-out rows", "replicates": replicates,
            "seed": seed, "accuracy_95_ci": [float(low[0]), float(high[0])],
            "macro_f1_95_ci": [float(low[1]), float(high[1])]}


def run(output_dir: Path, specs: dict[str, tuple[str, str]] = DEFAULT_SPECS, replicates: int = 5000) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    report: dict = {"scope": "recalculation from archived held-out predictions; no retraining performed", "models": {}}
    for name, (pred_rel, source_rel) in specs.items():
        pred_rows = _read(ROOT / pred_rel)
        y_true = np.array([int(r["true_label"]) for r in pred_rows])
        y_pred = np.array([int(r["predicted_label"]) for r in pred_rows])
        model = metrics(y_true, y_pred)
        model["bootstrap"] = bootstrap_ci(y_true, y_pred, replicates=replicates)
        confidences = [float(r["confidence"]) for r in pred_rows if r.get("confidence") not in (None, "")]
        model["calibration"] = {"available": bool(confidences), "input": "saved top-class confidence only; not class probability vector" if confidences else None,
                                "ece": None, "brier_score": None,
                                "note": "Top-label ECE is reported separately; Brier omitted because class probability vectors are unavailable." if confidences else "No probabilities available."}
        if confidences:
            model["mean_top_class_confidence"] = float(np.mean(confidences))
            predicted_confident = np.array([float(r["confidence"]) for r in pred_rows])
            correctness = (y_true == y_pred).astype(float)
            model["top_label_calibration"] = {
                "available": True,
                "method": "ECE with 10 equal-width bins of maximum class confidence; Brier unavailable because only maximum probability is saved",
                "ece_10_bins": _ece(predicted_confident, correctness, bins=10),
                "brier_score": None,
            }
        source = _read(ROOT / source_rel)
        if len(source) != len(pred_rows):
            raise ValueError(f"Prediction/source row count mismatch for {name}: {len(pred_rows)} != {len(source)}")
        source_labels = [int(row["label"]) for row in source]
        prediction_labels = [int(row["true_label"]) for row in pred_rows]
        if source_labels != prediction_labels:
            raise ValueError(f"Prediction rows do not align with source labels for {name}; refusing to attach source text or deduplicate")
        source_text = [r.get("text", "") for r in source]
        row_ids = [int(r.get("row_id", i)) for i, r in enumerate(pred_rows)]
        if "depression" in name:
            normalized = [_normalize_text(t) for t in source_text]
            train_rows = _read(ROOT / "backend/datasets/depression_v2/processed/train.csv")
            val_rows = _read(ROOT / "backend/datasets/depression_v2/processed/validation.csv")
            normalize_row = lambda r: _normalize_text(r.get("text", ""))
            train_norm = {normalize_row(r) for r in train_rows if normalize_row(r)}
            val_norm = {normalize_row(r) for r in val_rows if normalize_row(r)}
            seen: set[str] = set()
            keep = []
            duplicate_indices = []
            cross_split_indices = []
            for i, value in enumerate(normalized):
                if value and (value in train_norm or value in val_norm):
                    cross_split_indices.append(i)
                    continue
                if value and value in seen:
                    duplicate_indices.append(i)
                else:
                    if value:
                        seen.add(value)
                    keep.append(i)
            dedup_true = y_true[keep]
            dedup_pred = y_pred[keep]
            model["within_test_exact_normalized_duplicates_removed"] = len(duplicate_indices)
            model["train_or_validation_overlap_rows_removed"] = len(cross_split_indices)
            model["deduplicated_test_scope"] = "archived predictions restricted to first normalized test row not found in train or validation; same fitted model, not retraining; does not correct model-selection/training leakage or near-duplicate leakage"
            model["test_deduplicated_metrics"] = metrics(dedup_true, dedup_pred)
            model["test_deduplicated_bootstrap"] = bootstrap_ci(dedup_true, dedup_pred, replicates=replicates)
            model["test_text_overlap_with_train"] = sum(bool(value) and value in train_norm for value in normalized)
            model["test_text_overlap_with_validation"] = sum(bool(value) and value in val_norm for value in normalized)
        if "stress" in name:
            model["stress_false_negative_count"] = int(np.sum((y_true == 1) & (y_pred == 0)))
        stress_fn = []
        if "stress" in name:
            for i, row in enumerate(pred_rows):
                if int(row["true_label"]) == 1 and int(row["predicted_label"]) == 0:
                    source_idx = row_ids[i]
                    text = source_text[source_idx] if source_idx < len(source_text) else ""
                    stress_fn.append({"row_id": source_idx, "true_label": 1, "predicted_label": 0,
                                      "confidence": float(row["confidence"]) if row.get("confidence") else None,
                                      "text_excerpt": "OMITTED_FOR_PRIVACY",
                                      "error_theme": _error_theme(text)})
            model["stress_false_negative_count"] = len(stress_fn)
            model["stress_false_negative_examples"] = stress_fn[:20]
            model["stress_false_negative_theme_counts"] = dict(sorted(
                __import__("collections").Counter(item["error_theme"] for item in stress_fn).items()
            ))
        report["models"][name] = {"prediction_file": pred_rel, "source_split": source_rel, **model}
    json_path = output_dir / "HELDOUT_METRICS.json"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md = ["# Recalculated held-out classifier metrics", "", "Generated from saved predictions; no model retraining was performed.", "",
          "Bootstrap intervals use row-resampling with a fixed seed and percentile 95% bounds. Confidence files contain top-class confidence only, not full probability vectors, so calibration scores are not computed.", "",
          "| Model | N | Accuracy | Accuracy 95% CI | Macro-F1 | Macro-F1 95% CI |", "|---|---:|---:|---|---:|---|"]
    for name, m in report["models"].items():
        ci = m["bootstrap"]
        md.append(f"| {name} | {m['sample_count']} | {m['accuracy']:.4f} | {ci['accuracy_95_ci'][0]:.4f}–{ci['accuracy_95_ci'][1]:.4f} | {np.mean([v['f1'] for v in m['per_class'].values()]):.4f} | {ci['macro_f1_95_ci'][0]:.4f}–{ci['macro_f1_95_ci'][1]:.4f} |")
    depression = report["models"].get("depression_deberta")
    if depression:
        dedup = depression["test_deduplicated_metrics"]
        md.extend(["", "## Depression exact-overlap sensitivity check", "",
                   f"One of 1,148 test rows exactly matched normalized train text; zero matched validation and zero duplicated another test text. Excluding that train-overlap row from archived predictions yields accuracy {dedup['accuracy']:.4f} (N={dedup['sample_count']}); this is a sensitivity subset, not retraining and not validation against near-duplicate leakage.", ""])
    md.extend(["## Stress false negatives", ""])
    for name, m in report["models"].items():
        if "stress_false_negative_count" in m:
            md.append(f"- `{name}`: {m['stress_false_negative_count']} positive stress examples predicted negative (label 1→0). Theme counts: `{m.get('stress_false_negative_theme_counts', {})}`.")
    md.extend(["", "Per-class precision/recall/F1 and confusion matrices are in `HELDOUT_METRICS.json`.", ""])
    md.extend(["Stress false-negative counts and anonymized row IDs/error themes are in the JSON; text excerpts are deliberately omitted to avoid retaining sensitive narrative.", ""])
    (output_dir / "HELDOUT_METRICS.md").write_text("\n".join(md), encoding="utf-8")
    return report


def _error_theme(text: str) -> str:
    """Return coarse non-quoting theme for error analysis."""
    lower = text.casefold()
    if re.search(r"\b(money|rent|expensive|job|work|career|income|debt)\b", lower):
        return "financial_or_work_stressor"
    if re.search(r"\b(breakup|relationship|partner|marriage|divorce|family|parent)\b", lower):
        return "relationship_or_family_stressor"
    if re.search(r"\b(health|doctor|hospital|pain|illness|anxiety|depression|trauma)\b", lower):
        return "health_or_emotional_context"
    if re.search(r"\b(school|college|university|exam|study|teacher)\b", lower):
        return "education_stressor"
    return "other_or_contextual"


def _ece(confidence: np.ndarray, correct: np.ndarray, bins: int = 10) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    total = len(confidence)
    error = 0.0
    for i in range(bins):
        mask = (confidence >= edges[i]) & (confidence <= edges[i + 1] if i == bins - 1 else confidence < edges[i + 1])
        if np.any(mask):
            error += np.sum(mask) / total * abs(float(np.mean(correct[mask])) - float(np.mean(confidence[mask])))
    return float(error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "VALIDATION" / "classifiers")
    parser.add_argument("--replicates", type=int, default=5000)
    args = parser.parse_args()
    run(args.output, replicates=args.replicates)
    print(args.output / "HELDOUT_METRICS.md")
