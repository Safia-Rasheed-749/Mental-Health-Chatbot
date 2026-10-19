# -*- coding: utf-8 -*-
from types import SimpleNamespace

from app.ai.llm.validator import validate_response
from app.services.response_generation import concern_fallback, generate_validated_response, response_quality_reasons


class SequenceLLM:
    def __init__(self, answers):
        self.answers = iter(answers)
        self.calls = 0

    def invoke(self, messages):
        self.calls += 1
        answer = next(self.answers)
        if isinstance(answer, Exception):
            raise answer
        return SimpleNamespace(content=answer, response_metadata={"done_reason": "stop"})


def test_six_concern_fallbacks_are_language_safe_and_not_one_repeated_template():
    cases = [
        ("I feel stressed and worry about everything", "english", "stress"),
        ("I feel sad and no longer enjoy things", "english", "sadness"),
        ("Main bohat pareshan aur stressed hoon", "roman_urdu", "anxiety"),
        ("Mujhe apni parhai aur mustaqbil ki fikar hai", "roman_urdu", "academic"),
        ("میں اکثر اداس رہتی ہوں اور دلچسپی نہیں رہی", "urdu", "sadness"),
        ("مجھے اپنی پڑھائی اور مستقبل کی فکر ہے", "urdu", "academic"),
    ]
    results = []
    for question, language, concern in cases:
        answer = concern_fallback(question, language)
        assert validate_response(answer, language)["valid"]
        assert answer[-1] in ".!?؟۔"
        assert "Chunk" not in answer and "DETECTED MENTAL STATE" not in answer
        assert answer != "مجھے افسوس ہے کہ آپ کو بہت پریشانی ہو رہی ہے۔ ابھی آرام سے بیٹھیں اور چند بار آہستہ سانس لیں۔ اگر ممکن ہو تو کسی قابلِ اعتماد شخص سے بات کریں۔ کیا کوئی خاص بات آپ کی پریشانی بڑھا رہی ہے؟"
        results.append((concern, answer))
    assert results[3][1] != results[2][1]
    assert results[5][1] != results[4][1]


def test_valid_mocked_generation_is_returned_without_fallback():
    llm = SequenceLLM(["Choose one small study task and take a short break afterward. What feels urgent?"])
    answer, regenerated = generate_validated_response(
        llm, [], "I worry about exams", "english",
    )
    assert answer.startswith("Choose one small study task")
    assert regenerated is False
    assert llm.calls == 1


def test_invalid_or_truncated_output_retries_then_uses_concern_specific_fallback():
    llm = SequenceLLM([
        SimpleNamespace(content="What's one thing you think", response_metadata={"done_reason": "length"}),
        "I think",
        "I think",
    ])
    answer, regenerated = generate_validated_response(
        llm, [], "I feel sad and have stopped enjoying things", "english",
    )
    assert regenerated
    assert llm.calls == 3
    assert "losing interest" in answer
    assert validate_response(answer, "english")["valid"]


def test_generation_exception_returns_concern_aware_fallback_not_debug_text():
    llm = SequenceLLM([RuntimeError("private endpoint detail")] * 3)
    answer, regenerated = generate_validated_response(
        llm, [], "I am worried about exams and my future", "english",
    )
    assert regenerated
    assert "one small task" in answer
    assert "private endpoint detail" not in answer


def test_quality_gate_rejects_irrelevant_sadness_answer_and_weak_academic_advice():
    sadness_reasons = response_quality_reasons(
        "I feel sad and unmotivated and no longer enjoy things",
        "I am sorry to hear that. What has changed lately?",
        "english",
    )
    assert any("professional support" in reason for reason in sadness_reasons)
    academic_reasons = response_quality_reasons(
        "Mujhe apni parhai aur mustaqbil ki bohat fikar rehti hai",
        "Fikr karne ki aadat aapko apni parhai mein nahi rakh sakti. Take a break.",
        "roman_urdu",
    )
    assert any("practical step" in reason for reason in academic_reasons)
