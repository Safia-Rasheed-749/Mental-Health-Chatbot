# -*- coding: utf-8 -*-
from app.ai.llm.prompt import detect_language, get_prompt, resolve_response_language, history_messages
from app.ai.llm.validator import validate_response
from app.services.crisis_resources import get_crisis_response
from app.database.schemas import ChatRequest
from app.database.schemas import ChatResponse


def test_auto_script_detection_for_supported_inputs():
    assert detect_language("I feel anxious today") == "english"
    assert detect_language("Mujhe bohat anxiety ho rahi hai") == "roman_urdu"
    assert detect_language("مجھے بہت anxiety ہو رہی ہے") == "urdu"


def test_strict_language_rules_are_in_every_prompt():
    assert "STRICT OUTPUT LANGUAGE" in get_prompt("english").messages[0].prompt.template
    assert "Latin letters only" in get_prompt("roman_urdu").messages[0].prompt.template
    assert "Urdu script" in get_prompt("urdu").messages[0].prompt.template


def test_devanagari_is_rejected_for_urdu_output():
    assert not validate_response("यह ठीक है", "roman_urdu")["valid"]
    assert not validate_response("यह ठीक है", "urdu")["valid"]


def test_crisis_response_available_in_requested_urdu_script():
    response = get_crisis_response("HIGH", "urdu")
    assert "پاکستان" in response
    assert "1122" in response


def test_four_input_language_modes_resolve_consistently():
    # Typed Roman Urdu / Urdu and their speech transcripts use the same resolver.
    assert resolve_response_language("Mujhe bohat fikr hai") == "roman_urdu"
    assert resolve_response_language("مجھے بہت فکر ہے") == "urdu"
    assert resolve_response_language("Mujhe bohat fikr hai", input_language="roman_urdu") == "roman_urdu"
    assert resolve_response_language("مجھے بہت فکر ہے", input_language="urdu") == "urdu"


def test_auto_uses_prior_script_only_for_short_ambiguous_replies():
    history = [{"role": "user", "content": "Mujhe fikr ho rahi hai"}]
    assert resolve_response_language("Okay", history=history) == "roman_urdu"
    assert resolve_response_language("I am very stressed", history=history) == "english"
    assert resolve_response_language("Okay", "urdu", history=history) == "urdu"


def test_request_carries_mode_separately_from_language():
    typed = ChatRequest(message="Mujhe fikr hai", input_mode="text")
    spoken = ChatRequest(message="Mujhe fikr hai", input_mode="speech", input_language="roman_urdu")
    assert typed.input_mode == "text"
    assert spoken.input_mode == "speech"
    assert typed.response_language == "auto"


def test_history_is_role_preserving_and_latest_message_remains_separate():
    prior = history_messages([
        {"role": "user", "content": "Previous question"},
        {"role": "assistant", "content": "Previous answer"},
    ])
    messages = get_prompt("english").format_messages(
        context="", history=prior, question="I am very stressed",
    )
    assert [(item.type, item.content) for item in messages[-3:]] == [
        ("human", "Previous question"),
        ("ai", "Previous answer"),
        ("human", "I am very stressed"),
    ]


def test_chat_response_contract_exposes_estimates_separately_from_reply():
    assert {"response", "emotion", "emotion_confidence", "stress", "stress_confidence", "depression", "depression_confidence"} <= set(ChatResponse.model_fields)


def test_common_hindi_terms_are_rejected_in_roman_urdu():
    assert not validate_response("Samay parivaar ke saath baat karein. Main yahan hoon.", "roman_urdu")["valid"]


def test_urdu_quality_flags_known_bad_phrases_and_accepts_simple_urdu():
    assert not validate_response("یہ دل کی نہیں، ٹیکسچرز ہیں۔", "urdu")["valid"]
    awkward = "پریشانی کا احساس کیا ہے، اور کیا کیا جائے گا، یہ بات ہی اہم ہے۔"
    assert not validate_response(awkward, "urdu")["valid"]
    answer = "مجھے افسوس ہے کہ آپ کو بہت پریشانی ہو رہی ہے۔ آہستہ سانس لیں اور کسی قابلِ اعتماد شخص سے بات کریں۔ کیا کوئی خاص بات آپ کو پریشان کر رہی ہے؟"
    assert validate_response(answer, "urdu")["valid"]


def test_urdu_prompt_covers_anxiety_example_and_natural_vocabulary():
    system = get_prompt("urdu").messages[0].prompt.template
    assert "بے چینی" in system
    assert "تازہ ترین پیغام" in system
    assert "raw chunks" in system
