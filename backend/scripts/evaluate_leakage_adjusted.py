# -*- coding: utf-8 -*-
"""Evaluate saved classifier predictions after excluding audited train/eval overlaps.

Input predictions must be row-aligned to --evaluation-csv and include y_true plus
one probability column per class (prob_<label>). Exact overlaps and near-duplicate
candidates from dataset_audit.json are excluded from metrics; no model is retrained.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import unicodedata
from pathlib import Path


def _canon(path: str) -> str:
    return str(Path(path)).replace("\\", "/").casefold()


def _normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    value = re.sub(r"https?://\S+|www\.\S+", " URLTOKEN ", value)
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def _read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _macro_f1(y_true: list[str], y_pred: list[str], labels: list[str]) -> float:
    scores = []
    for label in labels:
        tp = sum(a == label and b == label for a, b in zip(y_true, y_pred))
        fp = sum(a != label and b == label for a, b in zip(y_true, y_pred))
        fn = sum(a == label and b != label for a, b in zip(y_true, y_pred))
        scores.append(2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0)
    return sum(scores) / len(scores)


def evaluate(prediction_csv: Path, train_csv: Path, evaluation_csv: Path, audit_json: Path,
             output_dir: Path, *, bins: int = 10, bootstrap: int = 2000, seed: int = 42) -> Path:
    fields, predictions = _read(prediction_csv)
    _, train_rows = _read(train_csv)
    _, evaluation_rows = _read(evaluation_csv)
    if len(predictions) != len(evaluation_rows):
        raise ValueError("Prediction rows must align one-to-one with evaluation CSV data rows.")
    true_col = next((key for key in ("y_true", "true_label", "label", "target") if key in fields), None)
    if true_col is None:
        raise ValueError("Predictions need a y_true/true_label/label/target column.")
    labels = sorted({row[true_col] for row in predictions})
    prob_cols = {label: next((c for c in (f"prob_{label}", f"probability_{label}", f"proba_{label}") if c in fields), None) for label in labels}
    if any(column is None for column in prob_cols.values()):
        raise ValueError(f"Full probability vectors required for Brier/calibration; expected columns prob_<class>. Found {fields}")
    text_col = next((c for c in _read(evaluation_csv)[0] if c.casefold() in {"text", "sentence", "question", "content", "utterance", "post"}), None)
    if not text_col:
        raise ValueError("Could not infer text column in evaluation CSV.")
    # Exact source text normalization matches audit_datasets.py.
    def normalized(value: str) -> str:
        return _normalize_text(value)

    train_norms = {normalized(row.get(text_col, "")) for row in train_rows}
    train_norms.discard("")
    audit = json.loads(audit_json.read_text(encoding="utf-8"))
    project_root = Path(__file__).resolve().parents[2]
    def audit_name(path: Path) -> str:
        return _canon(path.resolve().relative_to(project_root).as_posix()) if path.resolve().is_relative_to(project_root) else _canon(path.resolve().as_posix())
    train_path, eval_path = audit_name(train_csv), audit_name(evaluation_csv)
    excluded: dict[int, set[str]] = {}
    # Exhaustive text overlap locally, plus audit matches (which share the same normalized string).
    for i, row in enumerate(evaluation_rows):
        if normalized(row.get(text_col, "")) in train_norms:
            excluded.setdefault(i, set()).add("exact_train_overlap")
    requested = {train_path: "train", eval_path: "eval"}
    for pair in audit.get("near_duplicate_split_checks", []):
        left, right = _canon(pair["left"]), _canon(pair["right"])
        if {left, right} != {train_path, eval_path}:
            continue
        if pair.get("status") != "complete" or pair.get("skipped_comparisons"):
            raise ValueError(f"Near-duplicate audit is incomplete: {pair.get('status')}")
        for candidate in pair.get("pairs", []):
            row_number = candidate["left_row_1based"] if left == eval_path else candidate["right_row_1based"]
            excluded.setdefault(row_number - 2, set()).add(f"near_train_overlap_jaccard_{candidate['jaccard']:.6f}")
    keep = [i for i in range(len(predictions)) if i not in excluded]
    if not keep:
        raise ValueError("All evaluation examples were excluded; no metrics computed.")
    y = [predictions[i][true_col] for i in keep]
    probs = [[float(predictions[i][prob_cols[label]]) for label in labels] for i in keep]
    for row in probs:
        if any(p < 0 or p > 1 for p in row) or abs(sum(row) - 1) > 0.02:
            raise ValueError("Probability vectors must be within [0,1] and sum to approximately 1.")
    pred = [labels[max(range(len(labels)), key=lambda j: row[j])] for row in probs]
    accuracy = sum(a == b for a, b in zip(y, pred)) / len(y)
    macro_f1 = _macro_f1(y, pred, labels)
    brier = sum(sum((row[j] - (truth == label)) ** 2 for j, label in enumerate(labels)) for row, truth in zip(probs, y)) / len(y)
    rng = random.Random(seed)
    boot_acc, boot_f1 = [], []
    for _ in range(bootstrap):
        ix = [rng.randrange(len(y)) for _ in y]
        by, bp = [y[i] for i in ix], [pred[i] for i in ix]
        boot_acc.append(sum(a == b for a, b in zip(by, bp)) / len(by))
        boot_f1.append(_macro_f1(by, bp, labels))
    def ci(values: list[float]) -> list[float]:
        values.sort()
        return [values[int(.025 * (len(values) - 1))], values[int(.975 * (len(values) - 1))]]
    output_dir.mkdir(parents=True, exist_ok=True)
    calibration_path = output_dir / "calibration_curve.csv"
    cal_fields = ["class_label", "bin_left", "bin_right", "count", "mean_predicted_probability", "observed_fraction"]
    with calibration_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=cal_fields)
        writer.writeheader()
        for j, label in enumerate(labels):
            for b in range(bins):
                low, high = b / bins, (b + 1) / bins
                members = [i for i, row in enumerate(probs) if low <= row[j] < high or (b == bins - 1 and row[j] == 1)]
                if members:
                    writer.writerow({"class_label": label, "bin_left": low, "bin_right": high, "count": len(members),
                        "mean_predicted_probability": sum(probs[i][j] for i in members) / len(members),
                        "observed_fraction": sum(y[i] == label for i in members) / len(members)})
    manifest = {"scope": "archived predictions filtered after-the-fact; no retraining; near-duplicate candidates approximate",
        "prediction_file": str(prediction_csv), "training_file": str(train_csv), "evaluation_file": str(evaluation_csv),
        "sample_count_before": len(predictions), "sample_count_after": len(y), "excluded_count": len(excluded),
        "excluded_rows_1based_including_header": [i + 2 for i in sorted(excluded)],
        "exclusion_reasons": {str(i + 2): sorted(reason) for i, reason in excluded.items()},
        "labels": labels, "accuracy": accuracy, "macro_f1": macro_f1, "multiclass_brier_score": brier,
        "bootstrap": {"replicates": bootstrap, "seed": seed, "accuracy_95_ci": ci(boot_acc), "macro_f1_95_ci": ci(boot_f1)},
        "calibration_bins": bins, "calibration_curve_csv": str(calibration_path),
        "limitation": "This is a sensitivity analysis on predictions from the original fitted model. It does not replace deduplicated training, model selection without test leakage, or external validation."}
    report_path = output_dir / "leakage_adjusted_metrics.json"
    report_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return report_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("prediction-csv", "train-csv", "evaluation-csv", "audit", "output-dir"):
        parser.add_argument(f"--{option}", type=Path, required=True)
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.bins < 2 or args.bootstrap < 100:
        parser.error("--bins must be >=2 and --bootstrap >=100")
    try:
        print(evaluate(args.prediction_csv, args.train_csv, args.evaluation_csv, args.audit, args.output_dir, bins=args.bins, bootstrap=args.bootstrap, seed=args.seed))
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"METRIC EVALUATION REFUSED: {exc}") from exc
