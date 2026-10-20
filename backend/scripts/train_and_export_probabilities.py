# -*- coding: utf-8 -*-
"""Fine-tune a sequence classifier on audited deduplicated CSVs and export probabilities.

Example (from repository root):
  python backend/scripts/train_and_export_probabilities.py --task depression_v2 --data-dir VALIDATION/datasets/deduplicated/depression_v2 --model-name microsoft/deberta-v3-base --output-dir artifacts/retrained/depression_v2

Requires train_deduplicated.csv, validation_deduplicated.csv, test_deduplicated.csv
with text/label columns. The script never edits datasets or model artifacts in-place.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from pathlib import Path


def _load_rows(path: Path, text_column: str, label_column: str) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or text_column not in reader.fieldnames or label_column not in reader.fieldnames:
            raise ValueError(f"{path} must contain columns {text_column!r} and {label_column!r}")
        rows = [{"text": (row.get(text_column) or "").strip(), "label": (row.get(label_column) or "").strip()} for row in reader]
    rows = [row for row in rows if row["text"] and row["label"]]
    if not rows:
        raise ValueError(f"No labeled text rows in {path}")
    return rows


def export_probabilities(output_path: Path, texts: list[str], true_labels: list[int], probabilities: list[list[float]], label_names: list[str]) -> None:
    if not (len(texts) == len(true_labels) == len(probabilities)):
        raise ValueError("Prediction arrays must have equal row counts")
    if any(len(row) != len(label_names) for row in probabilities):
        raise ValueError("Probability vector width does not match label mapping")
    fields = ["text", "y_true", "y_pred", *[f"prob_{index}" for index in range(len(label_names))]]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for text, truth, row in zip(texts, true_labels, probabilities):
            if any(p < 0 or p > 1 for p in row) or abs(sum(row) - 1) > 1e-4:
                raise ValueError("Each probability vector must be in [0,1] and sum to 1")
            writer.writerow({"text": text, "y_true": truth, "y_pred": max(range(len(row)), key=row.__getitem__),
                             **{f"prob_{index}": f"{prob:.10f}" for index, prob in enumerate(row)}})


def train_and_export(data_dir: Path, output_dir: Path, *, model_name: str, task: str,
                     text_column: str = "text", label_column: str = "label", epochs: int = 3,
                     batch_size: int = 8, max_length: int = 256, seed: int = 42) -> Path:
    data_dir, output_dir = data_dir.resolve(), output_dir.resolve()
    split_paths = {name: data_dir / f"{name}_deduplicated.csv" for name in ("train", "validation", "test")}
    missing = [str(path) for path in split_paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Required deduplicated splits missing: " + ", ".join(missing))
    split_rows = {name: _load_rows(path, text_column, label_column) for name, path in split_paths.items()}
    label_names = sorted({row["label"] for rows in split_rows.values() for row in rows})
    if len(label_names) < 2:
        raise ValueError("At least two label classes are required")
    label_to_id = {name: idx for idx, name in enumerate(label_names)}
    output_dir.mkdir(parents=True, exist_ok=True)

    # Heavy ML dependencies are imported only when the user actually requests training.
    import numpy as np
    import torch
    from datasets import Dataset
    from transformers import (AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding,
                              Trainer, TrainingArguments, set_seed)

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    set_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=len(label_names),
        id2label={idx: name for name, idx in label_to_id.items()}, label2id=label_to_id)

    datasets = {}
    for split, rows in split_rows.items():
        dataset = Dataset.from_dict({"text": [r["text"] for r in rows],
                                     "labels": [label_to_id[r["label"]] for r in rows]})
        datasets[split] = dataset.map(lambda batch: tokenizer(batch["text"], truncation=True, max_length=max_length), batched=True)
        datasets[split].set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
    try:
        import inspect
        argument_name = "eval_strategy" if "eval_strategy" in inspect.signature(TrainingArguments).parameters else "evaluation_strategy"
    except (TypeError, ValueError):
        argument_name = "evaluation_strategy"
    args = TrainingArguments(output_dir=str(output_dir / "checkpoints"), num_train_epochs=epochs,
        learning_rate=2e-5, per_device_train_batch_size=batch_size, per_device_eval_batch_size=batch_size,
        weight_decay=0.01, save_strategy="epoch", load_best_model_at_end=True, metric_for_best_model="eval_loss",
        greater_is_better=False, report_to="none", seed=seed, data_seed=seed,
        **{argument_name: "epoch"})
    trainer = Trainer(model=model, args=args, train_dataset=datasets["train"], eval_dataset=datasets["validation"],
                      tokenizer=tokenizer, data_collator=DataCollatorWithPadding(tokenizer))
    trainer.train()
    test_output = trainer.predict(datasets["test"])
    probabilities = torch.softmax(torch.tensor(test_output.predictions), dim=-1).cpu().numpy().tolist()
    y_true = [label_to_id[row["label"]] for row in split_rows["test"]]
    pred_path = output_dir / f"{task}_test_predictions.csv"
    export_probabilities(pred_path, [row["text"] for row in split_rows["test"]], y_true, probabilities, label_names)
    final_model = output_dir / "model"
    trainer.save_model(str(final_model))
    tokenizer.save_pretrained(str(final_model))
    manifest = {"task": task, "base_model": model_name, "seed": seed, "epochs": epochs,
        "batch_size": batch_size, "max_length": max_length, "text_column": text_column,
        "label_column": label_column, "label_mapping": {str(v): k for k, v in label_to_id.items()},
        "split_rows": {name: len(rows) for name, rows in split_rows.items()},
        "split_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in split_paths.items()},
        "prediction_csv": str(pred_path), "prediction_sha256": hashlib.sha256(pred_path.read_bytes()).hexdigest(),
        "model_dir": str(final_model), "validation": "best checkpoint selected using validation split; test used only for final prediction export"}
    manifest_path = output_dir / "training_export_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if min(args.epochs, args.batch_size, args.max_length) < 1:
        parser.error("epochs, batch-size and max-length must be positive")
    try:
        print(train_and_export(args.data_dir, args.output_dir, model_name=args.model_name, task=args.task,
            text_column=args.text_column, label_column=args.label_column, epochs=args.epochs,
            batch_size=args.batch_size, max_length=args.max_length, seed=args.seed))
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"TRAIN/EXPORT FAILED: {exc}") from exc
