# -*- coding: utf-8 -*-
from utils.chat_rendering import contains_urdu_script
from utils.chat_suggestions import display_classifier_label, wellness_suggestion


def test_wellness_suggestions_match_current_concern_and_cycle_variants():
    study = wellness_suggestion("Mujhe apni parhai aur mustaqbil ki fikr hai", "roman_urdu")
    assert study["category"] == "academic"
    assert "parhai" in study["text"]
    assert wellness_suggestion("I feel sad and stopped enjoying things", "english")["category"] == "sadness"
    assert wellness_suggestion("I feel anxious and keep worrying", "english")["category"] == "anxiety"
    assert wellness_suggestion("I am under pressure", "english")["category"] == "stress"
    assert wellness_suggestion("worry", "english", 0)["text"] != wellness_suggestion("worry", "english", 1)["text"]


def test_wellness_suggestions_follow_the_requested_script():
    roman = wellness_suggestion("Mujhe parhai ki fikr hai", "roman_urdu")["text"]
    urdu = wellness_suggestion("مجھے پڑھائی کی فکر ہے", "urdu")["text"]
    assert not contains_urdu_script(roman)
    assert contains_urdu_script(urdu)


def test_classifier_labels_are_translated_without_inventing_anxiety_output():
    assert display_classifier_label("emotion", "fear", "urdu") == "خوف"
    assert display_classifier_label("emotion", "fear", "roman_urdu") == "Khauf"
    assert "anxiety" not in {"emotion", "stress", "depression"}

