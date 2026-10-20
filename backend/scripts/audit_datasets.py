# -*- coding: utf-8 -*-
"""Inventory dataset CSVs and report exact/near split overlap.

Examples (from repository root):
  python backend/scripts/audit_datasets.py
  python backend/scripts/audit_datasets.py --roots backend/datasets counsel_chat

Near-duplicate checks use normalized character 3–5-gram Jaccard with MinHash
LSH candidate generation. Any pair cap is explicitly reported; skipped work is
never reported as a clean audit.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
import hashlib
import heapq
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROOTS = [PROJECT_ROOT / "backend" / "datasets", PROJECT_ROOT / "counsel_chat"]
TEXT_NAMES = ("text", "sentence", "question", "content", "utterance", "post")
LABEL_NAMES = ("label", "emotion", "class", "target", "category", "sentiment")


def _norm(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    value = re.sub(r"https?://\S+|www\.\S+", " URLTOKEN ", value)
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def _choose_column(headers: list[str], candidates: tuple[str, ...]) -> str | None:
    lowered = {header.casefold(): header for header in headers}
    return next((lowered[name] for name in candidates if name in lowered), None)


def inspect_csv(path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="", errors="replace") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        text_column = _choose_column(headers, TEXT_NAMES)
        label_column = _choose_column(headers, LABEL_NAMES)
        text_values: list[str] = []
        text_hashes: list[str] = []
        label_values: list[str] = []
        label_counts: Counter = Counter()
        missing: Counter = Counter()
        row_counts: Counter = Counter()
        text_positions: dict[str, list[int]] = defaultdict(list)
        row_count = 0
        for row in reader:
            row_count += 1
            for header in headers:
                if not (row.get(header) or "").strip():
                    missing[header] += 1
            if label_column:
                label_value = (row.get(label_column, "") or "<blank>").strip()
                label_counts[label_value] += 1
                label_values.append(label_value)
            else:
                label_values.append("<unknown>")
            normalized_row = "\x1f".join(_norm(row.get(header, "")) for header in headers)
            row_counts[hashlib.sha256(normalized_row.encode("utf-8")).hexdigest()] += 1
            normalized_text = _norm(row.get(text_column, "")) if text_column else ""
            text_values.append(normalized_text)
            text_hash = hashlib.sha256(normalized_text.encode("utf-8")).hexdigest() if normalized_text else ""
            text_hashes.append(text_hash)
            if text_hash:
                text_positions[text_hash].append(row_count + 1)  # CSV header is row 1.
    exact_duplicate_rows = sum(count - 1 for count in row_counts.values() if count > 1)
    duplicate_groups = [
        {"normalized_text_sha256": text_hash,
         "source_rows_1based_including_header": source_rows,
         "labels_at_source_rows": [label_values[row_number - 2] for row_number in source_rows]}
        for text_hash, source_rows in text_positions.items() if len(source_rows) > 1
    ]
    exact_duplicate_texts = sum(len(source_rows) - 1 for source_rows in text_positions.values() if len(source_rows) > 1)
    try:
        display_path = str(path.resolve().relative_to(PROJECT_ROOT))
    except ValueError:
        display_path = str(path.resolve())
    return {
        "path": display_path,
        "headers": headers,
        "row_count": row_count,
        "text_column": text_column,
        "label_column": label_column,
        "label_balance": dict(sorted(label_counts.items())),
        "missing_values_by_column": missing,
        "exact_duplicate_rows_within_file": exact_duplicate_rows,
        "exact_duplicate_texts_within_file": exact_duplicate_texts,
        "exact_duplicate_text_groups_within_file": duplicate_groups,
        "texts": text_values,
        "text_hashes": text_hashes,
        "labels": label_values,
    }


def _near_duplicates(left: dict, right: dict, threshold: float, pair_cap: int) -> dict:
    left_texts, right_texts = left["texts"], right["texts"]
    comparisons = len(left_texts) * len(right_texts)
    result = {"left": left["path"], "right": right["path"], "threshold": threshold,
              "possible_comparisons": comparisons, "comparisons_performed": 0,
              "skipped_comparisons": [], "status": "complete", "pairs": [],
              "method": "normalized text; character 3–5-gram shingle Jaccard, candidate generation by bottom-32 MinHash LSH (8 bands × 4 values); exact normalized duplicates reported separately"}
    if not left["text_column"] or not right["text_column"]:
        result["status"] = "skipped_no_text_column"
        return result
    if not any(left_texts) or not any(right_texts):
        result["status"] = "skipped_empty_texts"
        return result
    def shingles(text: str) -> set[str]:
        padded = f"  {text}  "
        return {padded[i:i+n] for n in (3, 4, 5) for i in range(max(0, len(padded)-n+1))}

    def stable_hash(value: str) -> int:
        return int.from_bytes(hashlib.blake2b(value.encode("utf-8"), digest_size=8).digest(), "big")

    from functools import lru_cache
    @lru_cache(maxsize=50_000)
    def signature(text: str, size: int) -> tuple[int, ...] | None:
        if not text:
            return None
        return tuple(heapq.nsmallest(size, (stable_hash(item) for item in shingles(text))))

    bands = 8
    rows_per_band = 4
    signature_size = bands * rows_per_band
    buckets: dict[tuple[int, tuple[int, ...]], list[int]] = defaultdict(list)
    # Keep only compact signatures for the right corpus. Shingle sets are
    # constructed per record and discarded immediately to bound peak memory.
    for r, text in enumerate(right_texts):
        current_signature = signature(text, signature_size)
        if current_signature is None:
            continue
        for band in range(bands):
            start = band * rows_per_band
            buckets[(band, current_signature[start:start + rows_per_band])].append(r)

    limit = pair_cap if pair_cap > 0 else comparisons
    performed = candidate_count = 0
    omitted_start_left = omitted_start_right = None
    for l, text in enumerate(left_texts):
        current_signature = signature(text, signature_size)
        if current_signature is None:
            continue
        candidate_right: set[int] = set()
        for band in range(bands):
            start = band * rows_per_band
            candidate_right.update(buckets.get((band, current_signature[start:start + rows_per_band]), ()))
        for r in sorted(candidate_right):
            if performed >= limit:
                omitted_start_left, omitted_start_right = l, r
                break
            candidate_count += 1
            performed += 1
            if left_texts[l] == right_texts[r]:
                continue  # exact duplicates were already exhaustively recorded
            left_shingles = shingles(left_texts[l])
            right_shingles = shingles(right_texts[r])
            union = len(left_shingles | right_shingles)
            score = len(left_shingles & right_shingles) / union if union else 0.0
            if score >= threshold:
                result["pairs"].append({"left_row_1based": l + 2, "right_row_1based": r + 2,
                                        "jaccard": round(score, 6)})
        if omitted_start_left is not None:
            break
    result["candidate_pairs_examined"] = candidate_count
    result["comparisons_performed"] = performed
    if omitted_start_left is not None:
        # Exact skipped comparison scope, encoded as Cartesian row ranges to
        # avoid materializing millions of row-pair records.
        result["skipped_comparisons"] = [{
            "left_row_1based_start": omitted_start_left + 2,
            "left_row_1based_end": omitted_start_left + 2,
            "right_row_1based_start": omitted_start_right + 2,
            "right_row_1based_end": len(right_texts) + 1,
            "reason": "pair cap; exact remaining right-row span for this left row (candidate and noncandidate pairs)",
        }]
        if omitted_start_left + 1 < len(left_texts):
            result["skipped_comparisons"].append({
                "left_row_1based_start": omitted_start_left + 3,
                "left_row_1based_end": len(left_texts) + 1,
                "right_row_1based_start": 2,
                "right_row_1based_end": len(right_texts) + 1,
                "reason": "pair cap; exact remaining Cartesian row-pair scope",
            })
    result["status"] = "partial_pair_cap" if omitted_start_left is not None else "complete"
    return result


def audit(roots: list[Path], output_dir: Path, threshold: float, pair_cap: int) -> tuple[Path, Path]:
    paths = sorted({path for root in roots if root.exists() for path in root.rglob("*.csv") if path.is_file()})
    inspected = [inspect_csv(path) for path in paths]
    cross_exact = []
    grouped: dict[Path, list[dict]] = defaultdict(list)
    absolute_roots = [root.resolve() for root in roots if root.exists()]
    for item in inspected:
        file_path = (PROJECT_ROOT / item["path"]).resolve()
        matching_roots = [root for root in absolute_roots if root == file_path or root in file_path.parents]
        family_root = max(matching_roots, key=lambda root: len(root.parts)) if matching_roots else file_path.parent
        grouped[family_root].append(item)
    near_reports = []

    def split_role(path: str) -> str:
        stem = Path(path).stem.casefold()
        if re.search(r"valid|validation", stem):
            return "validation"
        if re.search(r"train", stem):
            return "train"
        if re.search(r"test", stem):
            return "test"
        if re.search(r"dev", stem):
            return "dev"
        return "unknown"

    for directory, group in grouped.items():
        split_files = [x for x in group if re.search(r"train|test|valid|dev", Path(x["path"]).stem, re.I)]
        for i, left in enumerate(split_files):
            left_set = {value for value in left["text_hashes"] if value}
            for right in split_files[i + 1:]:
                right_set = {value for value in right["text_hashes"] if value}
                overlap = sorted(left_set & right_set)
                if overlap:
                    left_positions: dict[str, list[int]] = defaultdict(list)
                    right_positions: dict[str, list[int]] = defaultdict(list)
                    for idx, value in enumerate(left["text_hashes"]):
                        if value:
                            left_positions[value].append(idx + 2)
                    for idx, value in enumerate(right["text_hashes"]):
                        if value:
                            right_positions[value].append(idx + 2)
                    cross_exact.append({"left": left["path"], "right": right["path"],
                                        "duplicate_text_count": len(overlap),
                                        "left_split_role": split_role(left["path"]),
                                        "right_split_role": split_role(right["path"]),
                                        "same_split_role_copy": split_role(left["path"]) == split_role(right["path"]),
                                        "possible_train_evaluation_leakage": (
                                            (split_role(left["path"]) == "train" and split_role(right["path"]) in {"test", "validation", "dev"})
                                            or (split_role(right["path"]) == "train" and split_role(left["path"]) in {"test", "validation", "dev"})
                                        ),
                                        "duplicate_records": [
                                            {"normalized_text_sha256": value,
                                             "left_source_rows_1based_including_header": left_positions[value],
                                             "left_labels": [left["labels"][row - 2] for row in left_positions[value]],
                                             "right_source_rows_1based_including_header": right_positions[value],
                                             "right_labels": [right["labels"][row - 2] for row in right_positions[value]]}
                                            for value in overlap
                                        ]})
                if (Path(left["path"]).parent == Path(right["path"]).parent
                        and ("train" in left["path"].casefold() or "train" in right["path"].casefold())):
                    near_reports.append(_near_duplicates(left, right, threshold, pair_cap))

    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "roots": [str(p) for p in roots],
        "near_duplicate_method": "NFKC/casefold/url-and-punctuation normalized character 3-5-gram Jaccard; bottom-32 MinHash LSH, 8 bands x 4 values; threshold is exact Jaccard on candidates",
        "near_duplicate_threshold": threshold,
        "max_pair_comparisons": pair_cap,
        "csv_files": [{k: v for k, v in item.items() if k not in {"texts", "text_hashes", "labels"}} for item in inspected],
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
        md_lines.extend(
            f"- `{x['left']}` ({x['left_split_role']}) vs `{x['right']}` ({x['right_split_role']}): "
            f"{x['duplicate_text_count']} normalized text hashes; "
            f"{'same-split source copies, not train/evaluation leakage' if x['same_split_role_copy'] else ('POTENTIAL train/evaluation leakage' if x['possible_train_evaluation_leakage'] else 'cross-split overlap; review provenance')}"
            for x in cross_exact
        )
    else:
        md_lines.append("No exact text duplicates found in the checked sibling split files.")
    md_lines.extend(["", "## Near-duplicate checks", "",
                     "Method: Unicode NFKC + casefold + URL replacement + punctuation removal + whitespace collapse; character 3–5-gram Jaccard evaluated for candidate pairs from bottom-32 MinHash LSH (8 bands × 4 values). Exact normalized matches are separately detected exhaustively. Candidate generation is approximate; near-duplicate recall is not guaranteed.", ""])
    for check in near_reports:
        md_lines.append(f"- `{check['left']}` vs `{check['right']}`: {check['status']}; {len(check.get('pairs', []))} flagged candidate pairs at Jaccard ≥ {threshold}; candidate similarities computed {check.get('comparisons_performed', 0)}; skipped ranges {len(check.get('skipped_comparisons', []))} (all-pairs possible: {check['possible_comparisons']}).")
        if check.get("skipped_comparisons"):
            md_lines.append(f"  - Exact skipped row-pair list: `dataset_audit.json` → `near_duplicate_split_checks` entry for this split pair.")
    md_lines.extend(["", "Similarity flags indicate possible leakage, not proof of it; inspect source data and labels before interpreting. Comparisons listed as skipped are unknown, not clean. See `dataset_audit.json` for row-level details.", ""])
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
