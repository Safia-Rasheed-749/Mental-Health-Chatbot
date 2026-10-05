"""Measure per-stage latency for the existing RAG chat pipeline.

Run from ``backend`` with its configured Python environment:
    python -m app.ai.evaluation_rag_llm.measure_latency

Each message is run three times; run 1 is a warm-up and runs 2-3 are measured.
Stage timing is observational and uses wrappers around the existing functions;
no application source files are modified.
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


TEST_MESSAGES = [
    "I feel sad today",
    "I am stressed about my exams",
    "Mujhe neend nahi aati",
    "I want to kill myself",
    "What is CBT?",
]
STAGES = [
    "crisis_check_ms",
    "emotion_classifier_ms",
    "stress_classifier_ms",
    "depression_classifier_ms",
    "rag_retrieval_ms",
    "prompt_assembly_ms",
    "llm_generation_ms",
    "total_ms",
]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    # Import only when running: model/service initialization failures are
    # captured in the results file rather than preventing an import of script.
    # Transformers 4.55 expects tokenizer_config.extra_special_tokens to be a
    # mapping, while the checked-in DeBERTa config stores it as a list. Its
    # standard pad/cls/sep tokens are independently configured, so normalize
    # only this obsolete optional field in memory for this measurement process.
    from transformers.tokenization_utils_base import PreTrainedTokenizerBase

    original_special_tokens = PreTrainedTokenizerBase._set_model_specific_special_tokens

    def compatible_special_tokens(self: Any, special_tokens: Any) -> None:
        if isinstance(special_tokens, list):
            special_tokens = {}
        original_special_tokens(self, special_tokens)

    PreTrainedTokenizerBase._set_model_specific_special_tokens = compatible_special_tokens

    from app.services import rag_chat_service as service

    samples: dict[str, list[float]] = {stage: [] for stage in STAGES}
    errors: list[dict[str, Any]] = []
    skipped: dict[str, int] = {stage: 0 for stage in STAGES[:-1]}
    current: dict[str, float] | None = None

    def wrap(owner: Any, name: str, stage: str) -> None:
        original = getattr(owner, name)

        def timed(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                return original(*args, **kwargs)
            finally:
                elapsed = (time.perf_counter() - start) * 1000
                if current is not None:
                    current[stage] = current.get(stage, 0.0) + elapsed

        # LangChain retrievers/chat models are Pydantic instances that reject
        # adding arbitrary fields via normal setattr. object.__setattr__ is
        # needed for this temporary, process-local instrumentation only.
        try:
            setattr(owner, name, timed)
        except (AttributeError, ValueError):
            object.__setattr__(owner, name, timed)

    # Both safety gates form the crisis check. The initial crisis detector can
    # short-circuit all later stages for crisis messages.
    wrap(service, "detect_crisis", "crisis_check_ms")
    wrap(service, "assess_crisis", "crisis_check_ms")
    wrap(service, "predict_emotion", "emotion_classifier_ms")
    wrap(service, "predict_stress", "stress_classifier_ms")
    wrap(service, "predict_depression", "depression_classifier_ms")
    wrap(service.retriever, "invoke", "rag_retrieval_ms")

    for name in ("build_context", "build_mental_state", "format_history", "get_prompt"):
        wrap(service, name, "prompt_assembly_ms")

    # PromptTemplate.format_messages lives on the instance returned by get_prompt.
    # Wrap the returned prompt to time prompt formatting too.
    original_get_prompt = service.get_prompt

    def timed_get_prompt(*args: Any, **kwargs: Any) -> Any:
        prompt = original_get_prompt(*args, **kwargs)
        original_format = prompt.format_messages

        def timed_format(*f_args: Any, **f_kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                return original_format(*f_args, **f_kwargs)
            finally:
                if current is not None:
                    current["prompt_assembly_ms"] = current.get("prompt_assembly_ms", 0.0) + (time.perf_counter() - start) * 1000

        try:
            prompt.format_messages = timed_format
        except (AttributeError, ValueError):
            object.__setattr__(prompt, "format_messages", timed_format)
        return prompt

    service.get_prompt = timed_get_prompt
    wrap(service.llm, "invoke", "llm_generation_ms")

    for message in TEST_MESSAGES:
        for run_index in range(3):
            current = {}
            started = time.perf_counter()
            error = None
            try:
                service.generate_chat_response(message)
            except Exception as exc:  # retain errors and continue other test cases
                error = f"{type(exc).__name__}: {exc}"
                errors.append({"message": message, "run": run_index + 1, "error": error})
            total = (time.perf_counter() - started) * 1000
            current["total_ms"] = total
            if run_index > 0 and error is None:
                for stage in STAGES:
                    if stage in current:
                        samples[stage].append(current[stage])
                for stage in STAGES[:-1]:
                    if stage not in current:
                        skipped[stage] += 1
            current = None

    summaries: dict[str, Any] = {}
    for stage, values in samples.items():
        summaries[stage] = (
            {
                "mean": round(statistics.mean(values), 3),
                "median": round(statistics.median(values), 3),
                "min": round(min(values), 3),
                "max": round(max(values), 3),
                "sample_count": len(values),
            }
            if values
            else {"mean": None, "median": None, "min": None, "max": None, "sample_count": 0}
        )

    result = {
        "project": "AI-Powered Mental Health Chatbot — FYP",
        "generated_at": datetime.now().astimezone().isoformat(),
        "timing_unit": "milliseconds",
        "messages": TEST_MESSAGES,
        "runs_per_message": 3,
        "warmup_runs_per_message": 1,
        "measurement_runs_per_message": 2,
        "stages": summaries,
        "untimed_stage_counts": skipped,
        "errors": errors,
        "notes": [
            "Crisis check combines detect_crisis and assess_crisis when the latter is reached.",
            "Crisis responses intentionally bypass classifiers, RAG, prompt assembly, and LLM generation.",
            "TOTAL is elapsed generate_chat_response time; classifier timings are sequential pipeline stage timings.",
            "Only successful measured runs are included in stage statistics.",
        ],
    }
    output = Path(__file__).resolve().parents[3] / "evaluation" / "latency_measurement.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"file": str(output), "stages": summaries, "errors": errors, "untimed_stage_counts": skipped}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Latency measurement failed before completion: {type(exc).__name__}: {exc}")
        raise
