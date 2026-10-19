# -*- coding: utf-8 -*-
"""Stable regression checks for established crisis phrases and clear negatives.

The complete matrix is evaluated separately and intentionally records misses;
it is not a claim that phrase matching covers all crisis language.
"""

import json
from pathlib import Path

from app.services.crisis_detector import detect_crisis

CASES = json.loads((Path(__file__).parent / "crisis_matrix.json").read_text(encoding="utf-8"))


def test_known_direct_crisis_phrases_remain_detected():
    case_ids = {"direct_en_01", "direct_en_02", "conditional_en_01", "code_switch_01", "roman_variant_01", "urdu_script_01"}
    cases = [case for case in CASES if case["id"] in case_ids]
    assert len(cases) == len(case_ids)
    assert all(detect_crisis(case["text"])["is_crisis"] for case in cases)


def test_clear_negation_and_nonpersonal_mention_are_not_triggered():
    case_ids = {"negated_01", "negated_02", "mention_01", "hyperbole_01", "ordinary_01"}
    cases = [case for case in CASES if case["id"] in case_ids]
    assert len(cases) == len(case_ids)
    assert all(not detect_crisis(case["text"])["is_crisis"] for case in cases)


def test_matrix_includes_known_challenging_categories():
    categories = {case["category"] for case in CASES}
    assert {"indirect", "conditional", "negation", "code_switched", "roman_urdu_variant", "urdu_script", "hyperbole"} <= categories
