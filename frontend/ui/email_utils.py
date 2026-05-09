# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from frontend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Email configuration from environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = os.getenv("SENDER_EMAIL")
SMTP_PASSWORD = os.getenv("SENDER_PASSWORD")

# Debug: Print if credentials are loaded
print(f"\n{'='*70}")
print(f"[EMAIL CONFIG] SMTP Server: {SMTP_SERVER}")
print(f"[EMAIL CONFIG] SMTP Port: {SMTP_PORT}")
print(f"[EMAIL CONFIG] SMTP Email: {SMTP_EMAIL}")
print(f"[EMAIL CONFIG] SMTP Password: {'*' * len(SMTP_PASSWORD) if SMTP_PASSWORD else 'NOT SET'}")
print(f"{'='*70}\n")

if not SMTP_EMAIL or not SMTP_PASSWORD:
    print("⚠️ WARNING: Email credentials not loaded from .env file!")
    print(f"   .env path: {env_path}")
    print(f"   .env exists: {env_path.exists()}")


def send_reset_email(to_email, code, username, is_signup=False):
    """
    Send password reset or signup verification email
    """
    print(f"\n{'='*70}")
    print(f"[EMAIL] Starting email send process")
    print(f"[EMAIL] To: {to_email}")
    print(f"[EMAIL] Code: {code}")
    print(f"[EMAIL] Username: {username}")
    print(f"[EMAIL] Is Signup: {is_signup}")
    print(f"{'='*70}\n")
    
    try:
        # Set subject and body based on type
        if is_signup:
            subject = "✉️ Verify Your Email - MindCare AI"
            body = f"""
Hello {username},

Thank you for signing up with MindCare AI!

Your verification code is:

    {code}

This code will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
MindCare AI Team
            """
        else:
            subject = "🔐 Password Reset Request - MindCare AI"
            body = f"""
Hello {username},

We received a request to reset your password.

Your verification code is:

    {code}

This code will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
MindCare AI Team
            """
        
        # Create message
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "plain"))
        
        print(f"[EMAIL] Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        print(f"[EMAIL] Starting TLS...")
        server.starttls()
        
        print(f"[EMAIL] Logging in as {SMTP_EMAIL}...")
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        
        print(f"[EMAIL] Sending email...")
        server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        
        print(f"[EMAIL] Closing connection...")
        server.quit()
        
        print(f"[EMAIL] ✅ EMAIL SENT SUCCESSFULLY to {to_email}")
        print(f"{'='*70}\n")
        
        return True, "Email sent successfully"
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP Authentication Failed: {str(e)}"
        print(f"[EMAIL] ❌ {error_msg}")
        print(f"[EMAIL] Check your Gmail App Password!")
        print(f"{'='*70}\n")
        return False, error_msg
        
    except smtplib.SMTPException as e:
        error_msg = f"SMTP Error: {str(e)}"
        print(f"[EMAIL] ❌ {error_msg}")
        print(f"{'='*70}\n")
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Email Error: {str(e)}"
        print(f"[EMAIL] ❌ {error_msg}")
        import traceback
        traceback.print_exc()
        print(f"{'='*70}\n")
        return False, error_msg