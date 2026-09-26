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
