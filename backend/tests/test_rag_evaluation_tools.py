# -*- coding: utf-8 -*-
import csv
import json
from types import SimpleNamespace
from io import BytesIO

import pytest

from app.ai.evaluation_rag_llm.evaluation_dataset import EVALUATION_DATASET
from app.ai.evaluation_rag_llm.evaluation_rubric import RUBRIC
from app.ai.evaluation_rag_llm import run_evaluation, summarize_retrieval, summarize_scores, prepare_review


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
    assert record["retrieved_chunk_ids"] == ["chunk-1#1"]
    assert record["prompt_sha256"] == "abc"
    assert record["scored"] is False

    score_sheet.write_text("human data must survive a rerun", encoding="utf-8")
    run_evaluation.run("test-model", "http://example.invalid")
    assert score_sheet.read_text(encoding="utf-8") == "human data must survive a rerun"


def test_occurrence_ids_disambiguate_identical_retrieved_chunks():
    assert run_evaluation._occurrence_ids(["same", "same", "other"]) == [
        "same#1", "same#2", "other#1"
    ]


def test_prepare_review_generates_enriched_reviewer_sheets_and_refuses_overwrite(tmp_path):
    raw = tmp_path / "raw.jsonl"
    with raw.open("w", encoding="utf-8") as handle:
        for item in EVALUATION_DATASET:
            handle.write(json.dumps({"test_id": item["test_id"], "question": item["user_question"],
                "expected_behavior": item["expected_behavior"], "model_tag": "test:1b", "prompt_sha256": "hash",
                "retrieved_chunk_ids": ["chunk-a", "chunk-a"],
                "retrieved_chunks": [{"chunk_id": "chunk-a", "text": "source passage"}],
                "display_response": "assistant answer", "scored": False, "status": "generated_unscored"}) + "\n")
    scores, retrieval = prepare_review.prepare(raw, tmp_path / "review")
    score_rows = list(csv.DictReader(scores.open(encoding="utf-8", newline="")))
    retrieval_rows = list(csv.DictReader(retrieval.open(encoding="utf-8", newline="")))
    assert len(score_rows) == len(retrieval_rows) == 60
    assert score_rows[0]["question"] and score_rows[0]["system_answer"] == "assistant answer"
    assert "source passage" in score_rows[0]["retrieved_chunks_json"]
    assert retrieval_rows[0]["retrieved_chunk_ids"] == "chunk-a#1;chunk-a#2"
    with pytest.raises(FileExistsError):
        prepare_review.prepare(raw, tmp_path / "review")


def test_score_summary_includes_low_score_diagnostics(tmp_path):
    score_path = tmp_path / "scores.csv"
    fields = ["test_id", "reviewer_role", *[f"{x}_score_1_to_5" for x in RUBRIC], "comments"]
    with score_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in EVALUATION_DATASET:
            for reviewer in ("reviewer_1", "reviewer_2"):
                writer.writerow({"test_id": item["test_id"], "reviewer_role": reviewer,
                    **{field: ("2" if item["test_id"] == "Q01" else "4") for field in fields[2:-1]},
                    "comments": "needs review" if item["test_id"] == "Q01" else ""})
    result = summarize_scores.summarize(score_path, tmp_path / "REPORT.md")
    text = result.read_text(encoding="utf-8")
    assert "Case diagnostics" in text and "needs review" in text and "context_relevance" in text


def test_retrieval_summary_counts_occurrences_and_accepts_explicit_none(tmp_path):
    input_path = tmp_path / "retrieval.csv"
    fields = ["test_id", "question", "retrieved_chunk_ids", "relevant_retrieved_chunk_ids",
              "all_relevant_chunk_ids", "precision_at_k", "coverage_recall", "reviewer_role", "comments"]
    with input_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for case in EVALUATION_DATASET:
            for reviewer in ("reviewer_1", "reviewer_2"):
                is_first = case["test_id"] == EVALUATION_DATASET[0]["test_id"]
                writer.writerow({
                    "test_id": case["test_id"], "question": case["user_question"],
                    "retrieved_chunk_ids": "duplicate#1;duplicate#2" if is_first else "chunk#1",
                    "relevant_retrieved_chunk_ids": "duplicate#2" if is_first else "NONE",
                    "all_relevant_chunk_ids": "duplicate#2;missed#1" if is_first else "NONE",
                    "reviewer_role": reviewer,
                })
    report_path = tmp_path / "retrieval-report.md"
    scored_path = tmp_path / "scored.csv"
    summarize_retrieval.summarize(input_path, report_path, scored_path)
    scored = list(csv.DictReader(scored_path.open(encoding="utf-8", newline="")))
    assert scored[0]["precision_at_k"] == "0.500000"
    assert scored[0]["coverage_recall"] == "0.500000"
    assert scored[2]["precision_at_k"] == "0.000000"
    assert scored[2]["coverage_recall"] == "0.000000"
