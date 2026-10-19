# -*- coding: utf-8 -*-
from app.services.chat_output import clean_user_response


def test_internal_chunks_and_classifier_metadata_are_replaced_not_exposed():
    leaked = "[Chunk 1] retrieved details\nStress: Yes Stress (100%)"
    for language in ("english", "roman_urdu", "urdu"):
        answer = clean_user_response(leaked, language)
        assert "Chunk" not in answer
        assert "Stress:" not in answer
        assert answer


def test_system_prompt_and_confidence_leaks_are_replaced():
    assert "SYSTEM PROMPT" not in clean_user_response("SYSTEM PROMPT: answer as follows", "english")
    assert "confidence:" not in clean_user_response("confidence: 99%", "english")


def test_clean_conversational_output_is_preserved():
    assert clean_user_response("I am here with you.", "english") == "I am here with you."


def test_raw_retrieved_passage_is_replaced():
    passage = "This is a long private knowledge passage that should never appear word for word in the chat response."
    answer = clean_user_response(passage, "english", passage, "I am worried about exams")
    assert answer != passage
    assert "task" in answer
