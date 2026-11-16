# -*- coding: utf-8 -*-
"""
email_service.py
================
Centralized email dispatch service for MindCare AI backend.
Handles transactional emails (password reset, account verification)
using configured SMTP server with TLS.
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_password_reset_email(to_email: str, username: str, reset_code: str) -> tuple[bool, str]:
    """
    Send password reset email containing a 6-digit verification code.

    Args:
        to_email: Recipient email address.
        username: Recipient display username.
        reset_code: 6-digit verification code.

    Returns:
        (success: bool, message: str)
    """
    if not settings.sender_email or not settings.sender_password:
        msg = "SMTP sender credentials not configured on backend."
        logger.warning("[EMAIL] %s Reset code for %s: %s (DEV LOG)", msg, to_email, reset_code)
        return True, "Email skipped (development fallback)"

    subject = "🔐 Password Reset Request — MindCare AI"
    body = f"""Hello {username},

We received a request to reset your MindCare AI account password.

Your 6-digit verification code is:

    {reset_code}

This code is valid for 1 hour. If you did not request a password reset, you can safely ignore this email.

Warm regards,
MindCare AI Support Team
"""

    try:
        msg = MIMEMultipart()
        msg["From"] = f"MindCare AI <{settings.sender_email}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=15) as server:
            server.starttls()
            server.login(settings.sender_email, settings.sender_password)
            server.sendmail(settings.sender_email, to_email, msg.as_string())

        logger.info("[EMAIL] Password reset email successfully sent to %s", to_email)
        return True, "Email sent successfully"

    except smtplib.SMTPAuthenticationError as exc:
        err = f"SMTP Authentication failed: {exc}"
        logger.error("[EMAIL] %s", err)
        return False, err
    except smtplib.SMTPException as exc:
        err = f"SMTP dispatch error: {exc}"
        logger.error("[EMAIL] %s", err)
        return False, err
    except Exception as exc:
        err = f"Unexpected email error: {exc}"
        logger.error("[EMAIL] %s", err)
        return False, err

