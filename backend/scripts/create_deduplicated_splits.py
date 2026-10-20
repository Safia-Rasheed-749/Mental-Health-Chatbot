# -*- coding: utf-8 -*-
"""Create clean *copies* of split CSVs using dataset_audit.json findings.

Example from repo root:
  python backend/scripts/create_deduplicated_splits.py --audit VALIDATION/datasets/classifier_splits/dataset_audit.json --split train=backend/datasets/depression_v2/processed/train.csv --split test=backend/datasets/depression_v2/processed/test.csv --output-dir VALIDATION/datasets/deduplicated/depression

Keeps the first exact duplicate within each split and removes evaluation rows
that overlap train exactly or with an audited near-duplicate candidate. Originals
are never modified. Review generated manifest and labels before retraining.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "").casefold()
    text = re.sub(r"https?://\S+|www\.\S+", " URLTOKEN ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def canonical(value: str) -> str:
    return str(Path(value)).replace("\\", "/").casefold()


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        return reader.fieldnames, list(reader)


def create(audit_path: Path, split_specs: list[str], output_dir: Path, text_column: str | None = None) -> Path:
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    split_data = {}
    for specification in split_specs:
        if "=" not in specification:
            raise ValueError(f"Expected split=CSV_PATH, got {specification!r}")
        name, file_name = specification.split("=", 1)
        path = Path(file_name).resolve()
        headers, rows = _read_csv(path)
        text_col = text_column or next((h for h in headers if h.casefold() in {"text", "sentence", "question", "content", "utterance", "post"}), None)
        if not text_col or text_col not in headers:
            raise ValueError(f"Cannot identify text column in {path}; supply --text-column")
        rel = canonical(path.relative_to(Path.cwd()).as_posix()) if path.is_relative_to(Path.cwd()) else canonical(path.as_posix())
        split_data[name] = {"path": path, "rel": rel, "headers": headers, "rows": rows, "text_col": text_col}
    if len(split_data) < 2 or "train" not in split_data:
        raise ValueError("Provide train plus at least one evaluation split, named with --split train=... --split test=...")
    audit_path_map = {canonical(item["path"]): item for item in audit.get("csv_files", [])}
    # Resolve audit relative paths against repository root (two parents above scripts).
    project_root = Path(__file__).resolve().parents[2]
    for item in split_data.values():
        rel = canonical(item["path"].relative_to(project_root).as_posix()) if item["path"].is_relative_to(project_root) else item["rel"]
        item["audit_path"] = rel
        if rel not in audit_path_map:
            raise ValueError(f"Split not found in audit manifest: {item['path']} (run audit_datasets.py first)")
    train = split_data["train"]
    # Source row numbers in the audit include the header (CSV row 1).
    drop_rows: dict[str, set[int]] = {name: set() for name in split_data}
    reasons: dict[str, dict[int, set[str]]] = {name: {} for name in split_data}

    def mark(name: str, source_row: int, reason: str) -> None:
        index = source_row - 2
        if 0 <= index < len(split_data[name]["rows"]):
            drop_rows[name].add(index)
            reasons[name].setdefault(index, set()).add(reason)

    # Remove exact copies after the first within every requested split.
    for name, item in split_data.items():
        first_by_text = {}
        for index, row in enumerate(item["rows"]):
            norm = normalize(row.get(item["text_col"], ""))
            if not norm:
                continue
            if norm in first_by_text:
                mark(name, index + 2, "within_split_exact_duplicate")
            else:
                first_by_text[norm] = index + 2

    requested = {item["audit_path"]: name for name, item in split_data.items()}
    for overlap in audit.get("exact_duplicate_texts_across_split_files", []):
        left_name, right_name = requested.get(canonical(overlap["left"])), requested.get(canonical(overlap["right"]))
        if not left_name or not right_name:
            continue
        for record in overlap.get("duplicate_records", []):
            for left_row in record.get("left_source_rows_1based_including_header", []):
                for right_row in record.get("right_source_rows_1based_including_header", []):
                    if left_name == "train" and right_name != "train":
                        mark(right_name, right_row, "train_exact_overlap")
                    elif right_name == "train" and left_name != "train":
                        mark(left_name, left_row, "train_exact_overlap")

    for pair in audit.get("near_duplicate_split_checks", []):
        left_name, right_name = requested.get(canonical(pair["left"])), requested.get(canonical(pair["right"]))
        if not left_name or not right_name or "train" not in {left_name, right_name}:
            continue
        if pair.get("status") != "complete" or pair.get("skipped_comparisons"):
            raise ValueError(f"Refusing partial near-duplicate audit for {pair['left']} vs {pair['right']}; rerun audit without pair caps first.")
        evaluation_name = right_name if left_name == "train" else left_name
        for candidate in pair.get("pairs", []):
            row_key = "right_row_1based" if left_name == "train" else "left_row_1based"
            mark(evaluation_name, candidate[row_key], f"train_near_overlap_jaccard_{candidate['jaccard']:.6f}")

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"source_audit": str(audit_path), "policy": "first normalized exact duplicate kept in each split; evaluation-side rows removed on exact train overlap and all audited near-duplicate candidate matches; source files untouched", "splits": {}}
    for name, item in split_data.items():
        output_path = output_dir / f"{name}_deduplicated.csv"
        keep = [row for index, row in enumerate(item["rows"]) if index not in drop_rows[name]]
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=item["headers"])
            writer.writeheader()
            writer.writerows(keep)
        manifest["splits"][name] = {
            "source": str(item["path"]), "output": str(output_path), "rows_before": len(item["rows"]),
            "rows_after": len(keep), "removed_count": len(drop_rows[name]),
            "removed_source_rows_1based_including_header": [index + 2 for index in sorted(drop_rows[name])],
            "removal_reasons": {str(index + 2): sorted(values) for index, values in sorted(reasons[name].items())},
            "sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
        }
    report_path = output_dir / "DEDUPLICATION_MANIFEST.json"
    report_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return report_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--split", action="append", required=True, help="Repeat: train=path.csv, test=path.csv, validation=path.csv")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--text-column", default=None)
    args = parser.parse_args()
    try:
        print(create(args.audit, args.split, args.output_dir, args.text_column))
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"DEDUPLICATION REFUSED: {exc}") from exc
