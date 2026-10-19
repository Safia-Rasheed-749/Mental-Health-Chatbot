# -*- coding: utf-8 -*-
from app.services.privacy import redact_sensitive_data


def test_redacts_email_phone_and_cnic():
    value = redact_sensitive_data(
        "Email me at test@example.com or call 0300-1234567. CNIC 35202-1234567-1"
    )
    assert "test@example.com" not in value
    assert "0300-1234567" not in value
    assert "35202-1234567-1" not in value
    assert "[EMAIL REDACTED]" in value
    assert "[PHONE REDACTED]" in value
    assert "[CNIC REDACTED]" in value


def test_redacts_common_email_phone_and_cnic_variants_in_mixed_text():
    source = "Email Test.User+tag@example.org; phone +92 300 123 4567; identity 35202 1234567 1."
    redacted = redact_sensitive_data(source)
    assert "Test.User+tag@example.org" not in redacted
    assert "+92 300 123 4567" not in redacted
    assert "35202 1234567 1" not in redacted
    assert redacted.count("[EMAIL REDACTED]") == 1
    assert redacted.count("[PHONE REDACTED]") == 1
    assert redacted.count("[CNIC REDACTED]") == 1


def test_redaction_preserves_non_sensitive_context_and_handles_non_string_input():
    assert redact_sensitive_data("I feel worried about exams.") == "I feel worried about exams."
    assert redact_sensitive_data(None) == ""
