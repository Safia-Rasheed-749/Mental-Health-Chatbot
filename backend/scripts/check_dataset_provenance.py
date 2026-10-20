# -*- coding: utf-8 -*-
"""Validate the structured dataset provenance register; never infer licenses.

Exit code 1 means one or more datasets still need human/source verification.
Run: python backend/scripts/check_dataset_provenance.py
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTER = ROOT / "VALIDATION" / "datasets" / "PROVENANCE.csv"
REQUIRED = ("upstream_name_or_owner", "upstream_url", "immutable_revision_or_version", "license_spdx_or_terms", "license_url", "license_evidence_path", "transformations", "split_method", "verification_status")


def check(path: Path) -> list[str]:
    problems = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("Provenance register is missing header")
        missing_columns = set(REQUIRED) - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
        rows = list(reader)
    if not rows:
        raise ValueError("Provenance register has no dataset rows")
    seen = set()
    for line, row in enumerate(rows, 2):
        dataset_id = (row.get("dataset_id") or "").strip()
        if not dataset_id or dataset_id in seen:
            problems.append(f"line {line}: missing or duplicate dataset_id {dataset_id!r}")
        seen.add(dataset_id)
        for column in REQUIRED:
            if not (row.get(column) or "").strip():
                problems.append(f"line {line} ({dataset_id}): {column} is blank")
        if (row.get("verification_status") or "").strip().upper() not in {"VERIFIED", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE"}:
            problems.append(f"line {line} ({dataset_id}): invalid verification_status")
        status = (row.get("verification_status") or "").strip().upper()
        if status != "VERIFIED":
            problems.append(f"line {line} ({dataset_id}): provenance/license status is {status or 'blank'}; source owner must verify it")
        for column, value in row.items():
            if value and value.strip().upper().startswith("PENDING"):
                problems.append(f"line {line} ({dataset_id}): {column} still has a pending placeholder")
        if status == "VERIFIED":
            for column in ("upstream_url", "immutable_revision_or_version", "license_spdx_or_terms", "license_url", "license_evidence_path"):
                if not (row.get(column) or "").strip():
                    problems.append(f"line {line} ({dataset_id}): VERIFIED requires {column}")
    return problems


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    args = parser.parse_args()
    issues = check(args.register)
    if issues:
        print(f"PROVENANCE INCOMPLETE: {len(issues)} issue(s)")
        print("\n".join(f"- {problem}" for problem in issues))
        raise SystemExit(1)
    print("All dataset provenance rows pass required-field checks.")
