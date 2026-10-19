# -*- coding: utf-8 -*-
import csv
import json
from types import SimpleNamespace
from io import BytesIO

import pytest

from app.ai.evaluation_rag_llm.evaluation_dataset import EVALUATION_DATASET
from app.ai.evaluation_rag_llm.evaluation_rubric import RUBRIC
from app.ai.evaluation_rag_llm import run_evaluation, summarize_scores


def test_ollama_preflight_requires_exact_tag(monkeypatch):
    response = BytesIO(json.dumps({"models": [{"name": "llama3.2:3b", "digest": "abc"}]}).encode())
    monkeypatch.setattr(run_evaluation.urllib.request, "urlopen", lambda *args, **kwargs: response)
    assert run_evaluation.ollama_preflight("llama3.2:3b", "127.0.0.1:11434")["digest"] == "abc"

    response = BytesIO(json.dumps({"models": [{"name": "llama3.2:3b", "digest": "abc"}]}).encode())
    monkeypatch.setattr(run_evaluation.urllib.request, "urlopen", lambda *args, **kwargs: response)
    with pytest.raises(RuntimeError, match="not installed"):
        run_evaluation.ollama_preflight("llama3.2:1b", "127.0.0.1:11434")


def test_score_summary_refuses_incomplete_scores(tmp_path):
    score_path = tmp_path / "scores.csv"
    with score_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["test_id", "reviewer_role", *[f"{x}_score_1_to_5" for x in RUBRIC]])
        writer.writeheader()
        writer.writerow({"test_id": EVALUATION_DATASET[0]["test_id"], "reviewer_role": "reviewer_1"})
    with pytest.raises(ValueError, match="missing"):
        summarize_scores.summarize(score_path, tmp_path / "REPORT.md")


def test_score_summary_requires_two_complete_raters_and_emits_kappa_report(tmp_path):
    score_path = tmp_path / "scores.csv"
    fields = ["test_id", "reviewer_role", *[f"{x}_score_1_to_5" for x in RUBRIC]]
    with score_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in EVALUATION_DATASET:
            for reviewer in ("reviewer_1", "reviewer_2"):
                writer.writerow({
                    "test_id": item["test_id"],
                    "reviewer_role": reviewer,
                    **{column: "4" for column in fields[2:]},
                })
    report = summarize_scores.summarize(score_path, tmp_path / "REPORT.md")
    assert "Cohen's κ" in report.read_text(encoding="utf-8")
    assert "30/30" in report.read_text(encoding="utf-8")


def test_runner_writes_unscored_raw_jsonl_and_does_not_overwrite_score_sheet(tmp_path, monkeypatch):
    fake_service = SimpleNamespace(generate_response_with_context=lambda question: {
        "response": "safe display text", "raw_response": "raw local model text",
        "context": "retrieved passage", "prompt_sha256": "abc",
        "retrieved_chunks": [{"chunk_id": "chunk-1", "text": "retrieved passage"}],
    })
    monkeypatch.setattr(run_evaluation, "OUTPUT", tmp_path)
    monkeypatch.setattr(run_evaluation, "ollama_preflight", lambda *args: {"name": "test-model", "digest": "digest"})
    monkeypatch.setitem(__import__("sys").modules, "app.services.rag_chat_service", fake_service)

    run_evaluation.run("test-model", "http://example.invalid")
    score_sheet = tmp_path / "scores.csv"
    rows = list(csv.DictReader(score_sheet.open(encoding="utf-8", newline="")))
    assert len(rows) == 2 * len(EVALUATION_DATASET)
    assert all(row["scored"] == "false" for row in rows)
    raw_path = next(tmp_path.glob("raw_run_*.jsonl"))
    record = json.loads(raw_path.read_text(encoding="utf-8").splitlines()[0])
    assert record["raw_response"] == "raw local model text"
    assert record["retrieved_chunk_ids"] == ["chunk-1"]
    assert record["prompt_sha256"] == "abc"
    assert record["scored"] is False

    score_sheet.write_text("human data must survive a rerun", encoding="utf-8")
    run_evaluation.run("test-model", "http://example.invalid")
    assert score_sheet.read_text(encoding="utf-8") == "human data must survive a rerun"
