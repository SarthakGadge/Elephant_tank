import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils import timezone
import random
 
# Email account credentials
SMTP_SERVER = "smtp.office365.com"
IMAP_SERVER = "outlook.office365.com"
EMAIL = "support@elephant-tank.com"
PASSWORD = "2024@Tdtl"
 
# Auto-reply content

def check_and_reply(user):
    
    otp = str(random.randint(1000, 9999))

    # Save OTP in the user model or OTP table
    user.otp = otp
    user.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
    user.max_otp_try -= 1
    if user.max_otp_try <= 0:
        user.otp_max_out = timezone.now() + timezone.timedelta(hours=1)
    else:
        user.max_otp_try -= 1
    user.save()

    
    AUTO_REPLY_SUBJECT = "Re: Your Email to Elephant Tank Support"
    AUTO_REPLY_BODY = """
Thank you for reaching out to Elephant Tank Support.
 
We have received your email and will respond within 24-48 hours. For urgent inquiries, please call us at [Your Contact Number].
 
Best regards,
Elephant Tank Support Team
"""
 
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
 
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
 
        for email_id in email_ids:
            # Fetch the email
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
 
                    # Get sender's email
                    sender_email = msg["From"]
 
                    # Create auto-reply email
                    reply = MIMEMultipart()
                    reply["From"] = EMAIL
                    reply["To"] = sender_email
                    reply["Subject"] = AUTO_REPLY_SUBJECT
                    reply.attach(MIMEText(AUTO_REPLY_BODY, "plain"))
 
                    # Send the reply
                    with smtplib.SMTP(SMTP_SERVER, 587) as smtp:
                        smtp.starttls()
                        smtp.login(EMAIL, PASSWORD)
                        smtp.sendmail(EMAIL, sender_email, reply.as_string())
                        print(f"Auto-reply sent to {sender_email}")
 
        mail.logout()
 
    except Exception as e:
        print(f"Error: {e}")
 
