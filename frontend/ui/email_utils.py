# email_utils.py
import smtplib
import random
import string
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
APP_URL = os.getenv("APP_URL", "http://localhost:8501")

def generate_reset_token():
    """Generate a secure random token for password reset"""
    # Method 1: Simple 6-digit code (user-friendly)
    reset_code = ''.join(random.choices(string.digits, k=6))
    
    # Method 2: Secure URL token (more secure but less user-friendly)
    secure_token = secrets.token_urlsafe(32)
    
    return {
        'code': reset_code,          # For user to type
        'token': secure_token,       # For URL-based reset
        'expiry': datetime.now() + timedelta(hours=1)  # 1 hour expiry
    }

def send_reset_email(to_email, reset_code, username):
    """
    Send password reset email with professional template
    """
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🔐 Password Reset Request - AI Therapist"
        msg['From'] = f"AI Therapist <{SENDER_EMAIL}>"
        msg['To'] = to_email
        
        # HTML Email Template (Professional)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0; padding:0; background-color:#f4f7fc; font-family: 'Segoe UI', Roboto, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:0 auto; background-color:#ffffff; border-radius:24px; margin-top:40px; box-shadow:0 20px 40px rgba(0,0,0,0.08);">
                <!-- Header with gradient -->
                <tr>
                    <td style="background:linear-gradient(135deg, #4A90E2, #6B5B95); padding:30px; border-radius:24px 24px 0 0; text-align:center;">
                        <h1 style="color:white; margin:0; font-size:28px; font-weight:600;">AI Therapist</h1>
                        <p style="color:rgba(255,255,255,0.9); margin:10px 0 0 0;">Your Safe Space for Healing</p>
                    </td>
                </tr>
                
                <!-- Content -->
                <tr>
                    <td style="padding:40px 30px;">
                        <h2 style="color:#1e293b; margin:0 0 20px 0;">Password Reset Request</h2>
                        <p style="color:#475569; font-size:16px; line-height:1.6; margin:0 0 20px 0;">
                            Hello <strong>{username}</strong>,<br><br>
                            We received a request to reset your password. Use the verification code below to proceed:
                        </p>
                        
                        <!-- Reset Code Box -->
                        <div style="background:#f8fafc; border-radius:16px; padding:25px; text-align:center; border:1px solid #e2e8f0; margin:30px 0;">
                            <div style="font-size:14px; color:#64748b; margin-bottom:10px;">Your Verification Code</div>
                            <div style="font-size:48px; letter-spacing:8px; font-weight:700; color:#4A90E2; font-family:monospace;">
                                {reset_code}
                            </div>
                            <div style="font-size:13px; color:#94a3b8; margin-top:15px;">
                                This code will expire in 1 hour
                            </div>
                        </div>
                        
                        <!-- Alternative Link -->
                        <div style="text-align:center; margin:30px 0;">
                            <p style="color:#64748b; font-size:14px;">Or click the button below:</p>
                            <a href="{APP_URL}/reset-password?code={reset_code}&email={to_email}" 
                               style="display:inline-block; background:linear-gradient(135deg, #4A90E2, #6B5B95); color:white; text-decoration:none; padding:14px 32px; border-radius:30px; font-weight:600; margin:10px 0;">
                                Reset Password
                            </a>
                        </div>
                        
                        <!-- Security Notice -->
                        <div style="border-top:1px solid #e2e8f0; margin:30px 0 0 0; padding:20px 0 0 0;">
                            <p style="color:#94a3b8; font-size:13px; margin:0;">
                                ⚠️ If you didn't request this, please ignore this email or contact support.<br>
                                Never share this code with anyone.
                            </p>
                        </div>
                    </td>
                </tr>
                
                <!-- Footer -->
                <tr>
                    <td style="background:#f8fafc; padding:20px 30px; border-radius:0 0 24px 24px; text-align:center; border-top:1px solid #e2e8f0;">
                        <p style="color:#94a3b8; font-size:13px; margin:0;">
                            © 2024 AI Therapist. All rights reserved.<br>
                            Need help? Contact us at support@aitherapist.com
                        </p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        # Plain text alternative
        text = f"""
        Password Reset Request - AI Therapist
        
        Hello {username},
        
        We received a request to reset your password.
        
        Your verification code is: {reset_code}
        
        This code will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        
        © 2024 AI Therapist
        """
        
        # Attach parts
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "Reset email sent successfully"
        
    except Exception as e:
        print(f"Email sending error: {e}")
        return False, f"Failed to send email: {str(e)}"