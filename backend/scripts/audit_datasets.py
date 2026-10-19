# -*- coding: utf-8 -*-
"""Inventory dataset CSVs and report exact/near split overlap.

Examples (from repository root):
  python backend/scripts/audit_datasets.py
  python backend/scripts/audit_datasets.py --roots backend/datasets counsel_chat

Near-duplicate checks use character n-gram TF-IDF cosine similarity at >= .95.
Large train/test pairs above the configured comparison cap are explicitly marked
skipped; a skipped comparison is never reported as a clean audit.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROOTS = [PROJECT_ROOT / "backend" / "datasets", PROJECT_ROOT / "counsel_chat"]
TEXT_NAMES = ("text", "sentence", "question", "content", "utterance", "post")
LABEL_NAMES = ("label", "emotion", "class", "target", "category", "sentiment")


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").casefold()).strip()


def _choose_column(headers: list[str], candidates: tuple[str, ...]) -> str | None:
    lowered = {header.casefold(): header for header in headers}
    return next((lowered[name] for name in candidates if name in lowered), None)


def inspect_csv(path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="", errors="replace") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = list(reader)
    text_column = _choose_column(headers, TEXT_NAMES)
    label_column = _choose_column(headers, LABEL_NAMES)
    normalized_rows = [
        "\x1f".join(_norm(row.get(header, "")) for header in headers)
        for row in rows
    ]
    text_values = [_norm(row.get(text_column, "")) for row in rows] if text_column else []
    label_counts = Counter((row.get(label_column, "") or "<blank>").strip() for row in rows) if label_column else Counter()
    missing = {
        header: sum(not (row.get(header) or "").strip() for row in rows)
        for header in headers
    }
    row_counts = Counter(normalized_rows)
    exact_duplicate_rows = sum(count - 1 for count in row_counts.values() if count > 1)
    exact_duplicate_texts = sum(count - 1 for count in Counter(x for x in text_values if x).values() if count > 1)
    return {
        "path": str(path.relative_to(PROJECT_ROOT)),
        "headers": headers,
        "rows": rows,
        "row_count": len(rows),
        "text_column": text_column,
        "label_column": label_column,
        "label_balance": dict(sorted(label_counts.items())),
        "missing_values_by_column": missing,
        "exact_duplicate_rows_within_file": exact_duplicate_rows,
        "exact_duplicate_texts_within_file": exact_duplicate_texts,
        "texts": text_values,
    }


def _near_duplicates(left: dict, right: dict, threshold: float, pair_cap: int) -> dict:
    left_texts, right_texts = left["texts"], right["texts"]
    comparisons = len(left_texts) * len(right_texts)
    result = {"left": left["path"], "right": right["path"], "threshold": threshold,
              "possible_comparisons": comparisons, "status": "complete", "pairs": []}
    if not left["text_column"] or not right["text_column"]:
        result["status"] = "skipped_no_text_column"
        return result
    if comparisons > pair_cap:
        result["status"] = "skipped_pair_cap"
        return result
    if not any(left_texts) or not any(right_texts):
        result["status"] = "skipped_empty_texts"
        return result
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
    except ImportError:
        result["status"] = "skipped_scikit_learn_unavailable"
        return result
    all_texts = left_texts + right_texts
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
    matrix = vectorizer.fit_transform(all_texts)
    n_left = len(left_texts)
    similarity = matrix[:n_left] @ matrix[n_left:].T
    coo = similarity.tocoo()
    result["pairs"] = [
        {"left_row_1based": int(row) + 2, "right_row_1based": int(col) + 2, "cosine": round(float(score), 6)}
        for row, col, score in zip(coo.row, coo.col, coo.data)
        if score >= threshold and left_texts[row] and right_texts[col]
    ]
    return result


def audit(roots: list[Path], output_dir: Path, threshold: float, pair_cap: int) -> tuple[Path, Path]:
    paths = sorted({path for root in roots if root.exists() for path in root.rglob("*.csv") if path.is_file()})
    inspected = [inspect_csv(path) for path in paths]
    cross_exact = []
    grouped: dict[Path, list[dict]] = defaultdict(list)
    for item in inspected:
        file_path = PROJECT_ROOT / item["path"]
        grouped[file_path.parent].append(item)
    near_reports = []
    for directory, group in grouped.items():
        split_files = [x for x in group if re.search(r"train|test|valid|dev", Path(x["path"]).stem, re.I)]
        for i, left in enumerate(split_files):
            left_set = {value for value in left["texts"] if value}
            for right in split_files[i + 1:]:
                right_set = {value for value in right["texts"] if value}
                overlap = sorted(left_set & right_set)
                if overlap:
                    cross_exact.append({"left": left["path"], "right": right["path"],
                                        "duplicate_text_count": len(overlap), "examples": overlap[:5]})
                if "train" in left["path"].casefold() or "train" in right["path"].casefold():
                    near_reports.append(_near_duplicates(left, right, threshold, pair_cap))

    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "roots": [str(p) for p in roots],
        "near_duplicate_method": "character n-gram TF-IDF cosine similarity",
        "near_duplicate_threshold": threshold,
        "max_pair_comparisons": pair_cap,
        "csv_files": [{k: v for k, v in item.items() if k not in {"rows", "texts"}} for item in inspected],
        "exact_duplicate_texts_across_split_files": cross_exact,
        "near_duplicate_split_checks": near_reports,
        "limitations": "Near-duplicate comparisons marked skipped are not evidence of no leakage. Results are text-overlap flags, not a legal or dataset-provenance audit.",
    }
    json_path = output_dir / "dataset_audit.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    md_lines = ["# Dataset audit", "", f"Generated (UTC): {payload['generated_at_utc']}", "",
                "This report inventories CSV files, missing fields, class balance, exact duplicates, and near-duplicate train/split overlap.", "",
                "| CSV | Rows | Text | Label | Exact row dupes | Exact text dupes |", "|---|---:|---|---|---:|---:|"]
    for item in inspected:
        md_lines.append(f"| `{item['path']}` | {item['row_count']} | {item['text_column'] or 'not inferred'} | {item['label_column'] or 'not inferred'} | {item['exact_duplicate_rows_within_file']} | {item['exact_duplicate_texts_within_file']} |")
    md_lines.extend(["", "## Cross-split exact duplicate text", ""])
    if cross_exact:
        md_lines.extend(f"- `{x['left']}` vs `{x['right']}`: {x['duplicate_text_count']} duplicate texts" for x in cross_exact)
    else:
        md_lines.append("No exact text duplicates found in the checked sibling split files.")
    md_lines.extend(["", "## Near-duplicate checks", ""])
    for check in near_reports:
        md_lines.append(f"- `{check['left']}` vs `{check['right']}`: {check['status']}; {len(check.get('pairs', []))} pairs at cosine ≥ {threshold} (possible comparisons: {check['possible_comparisons']}).")
    md_lines.extend(["", "Skipped comparisons are unknown, not clean. Similarity flags require manual review. See `dataset_audit.json` for exact details.", ""])
    md_path = output_dir / "DATASET_AUDIT.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    return json_path, md_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roots", nargs="*", type=Path, default=DEFAULT_ROOTS)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "VALIDATION" / "datasets")
    parser.add_argument("--threshold", type=float, default=0.95)
    parser.add_argument("--pair-cap", type=int, default=2_000_000)
    args = parser.parse_args()
    roots = [p if p.is_absolute() else PROJECT_ROOT / p for p in args.roots]
    json_path, md_path = audit(roots, args.output, args.threshold, args.pair_cap)
    print(json_path)
    print(md_path)
