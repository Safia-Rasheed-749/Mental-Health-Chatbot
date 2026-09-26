from app.services.crisis_detector import detect_crisis


def test_high_risk_english_is_detected():
    result = detect_crisis("I want to kill myself tonight")
    assert result["is_crisis"] is True
    assert result["severity"] == "HIGH"


def test_normal_message_is_not_crisis():
    result = detect_crisis("I am stressed about my exam")
    assert result["is_crisis"] is False
    assert result["severity"] is None
