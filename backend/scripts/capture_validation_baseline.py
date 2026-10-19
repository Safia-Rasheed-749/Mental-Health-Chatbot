# -*- coding: utf-8 -*-
"""Capture local versions, Git state, and SHA-256 manifests for validation.

This does not create a tag or commit. If the worktree is dirty, the generated
artifact says so rather than implying a reproducible tagged baseline.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = PROJECT_ROOT / "VALIDATION" / "baseline"


def command_output(command: list[str]) -> str:
    try:
        result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30)
        return (result.stdout + result.stderr).strip() if result.returncode == 0 else f"unavailable (exit {result.returncode}): {(result.stderr or result.stdout).strip()}"
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {exc}"


def hash_tree(paths: list[Path], name: str) -> Path:
    rows = []
    for root in paths:
        if not root.exists():
            continue
        files = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
        for path in files:
            digest = hashlib.sha256()
            size = 0
            with path.open("rb") as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(block)
                    size += len(block)
            rows.append({"path": str(path.relative_to(PROJECT_ROOT)), "bytes": size, "sha256": digest.hexdigest()})
    destination = OUTPUT / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return destination


def capture() -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    git_commit = command_output(["git", "rev-parse", "HEAD"])
    git_status = command_output(["git", "status", "--short"])
    freeze = command_output([sys.executable, "-m", "pip", "freeze"])
    (OUTPUT / "pip-freeze.txt").write_text(freeze + "\n", encoding="utf-8")

    models = PROJECT_ROOT / "backend" / "models"
    datasets = [PROJECT_ROOT / "backend" / "datasets", PROJECT_ROOT / "counsel_chat"]
    knowledge = PROJECT_ROOT / "backend" / "knowledge_base"
    hash_tree([models], "MODEL_HASHES.json")
    hash_tree(datasets, "DATASET_HASHES.json")
    hash_tree([knowledge], "KB_HASHES.json")

    try:
        import psycopg2
        postgres_driver = getattr(psycopg2, "__version__", "installed")
    except ImportError:
        postgres_driver = "not installed in this Python environment"
    snapshot = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit,
        "git_worktree_status": git_status or "clean",
        "baseline_tag_created": False,
        "baseline_tag_note": "No tag was created; this script is intentionally non-destructive and a dirty worktree cannot identify a clean reproducible commit.",
        "python": sys.version,
        "platform": platform.platform(),
        "postgresql_client": command_output(["psql", "--version"]),
        "postgresql_driver": postgres_driver,
        "ollama_version": command_output(["ollama", "--version"]),
        "ollama_models": command_output(["ollama", "list"]),
        "python_environment": str(sys.executable),
        "requirements_files": [
            "backend/requirements.txt",
            "frontend/requirements.txt",
            "VALIDATION/baseline/pip-freeze.txt is the resolved environment snapshot used for this capture",
        ],
    }
    path = OUTPUT / "environment.json"
    path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    (OUTPUT / "BASELINE.md").write_text(
        "# Validation baseline capture\n\n"
        f"Captured: {snapshot['captured_at_utc']}\n\n"
        f"- Git commit: `{git_commit}`\n"
        f"- Worktree: {'clean' if not git_status else 'dirty; see environment.json'}\n"
        "- A Git tag was intentionally not created because the existing worktree includes uncommitted user/project changes.\n"
        "- Python package snapshot: `pip-freeze.txt`\n"
        "- SHA-256 manifests: `MODEL_HASHES.json`, `DATASET_HASHES.json`, and `KB_HASHES.json`\n"
        "- Runtime availability probes: `environment.json`\n\n"
        "A captured dirty-tree environment does not establish a reproducible clean checkout. Commit/tag only after the owner reviews and approves the full diff.\n",
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    print(capture())
