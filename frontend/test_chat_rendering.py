# -*- coding: utf-8 -*-
from utils.chat_rendering import assistant_markup, contains_urdu_script


def test_urdu_content_is_rtl_and_preserves_character_order():
    phrase = "مجھے بہت پریشانی ہو رہی ہے"
    rendered = assistant_markup(phrase, "urdu")
    assert 'dir="rtl"' in rendered
    assert "urdu-text" in rendered
    assert phrase in rendered


def test_urdu_markdown_lists_and_headings_render_as_html():
    rendered = assistant_markup("## سکون کے لیے\n\n1. آہستہ سانس لیں\n2. مدد لیں", "urdu")
    assert "<h2>" in rendered
    assert "<ol>" in rendered and "<li>" in rendered


def test_long_urdu_paragraph_and_mixed_english_keep_rtl_order():
    text = ("مجھے بے چینی محسوس ہو رہی ہے، اور میں سکون چاہتا ہوں۔ " * 8) + "کیا breathing exercise مدد کر سکتی ہے؟"
    rendered = assistant_markup(text, "urdu")
    assert 'dir="rtl"' in rendered
    assert "breathing exercise" in rendered
    assert text in rendered


def test_english_and_roman_urdu_stay_ltr_and_untrusted_html_is_removed():
    assert 'dir="ltr"' in assistant_markup("Hello **there**", "english")
    assert 'dir="ltr"' in assistant_markup("Mujhe pareshani hai", "roman_urdu")
    assert "<script>" not in assistant_markup("<script>alert(1)</script>ٹھیک", "urdu")


def test_unicode_script_detection():
    assert contains_urdu_script("پریشانی")
    assert not contains_urdu_script("Mujhe pareshani hai")
