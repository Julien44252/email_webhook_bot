# email_sender.py
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()

EMAIL    = os.getenv("EMAIL")          # ou EMAIL_ADDRESS si tu préfères
PASSWORD = os.getenv("EMAIL_PASSWORD")
DEST     = os.getenv("TO_EMAIL")       # ou DEST_EMAIL, selon ce que tu as dans .env

# DEBUG : on vérifie bien qu’on a chargé les bonnes vars
print("🔍 DEBUG ENV:",
      f"EMAIL={EMAIL!r}",
      f"DEST={DEST!r}",
      f"PASSWORD set? {bool(PASSWORD)}")

def send_email(subject, body):
    print("🔔 DEBUG: send_email called")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"]    = EMAIL
    msg["To"]      = DEST

    print("🔗 DEBUG: Connecting to smtp.gmail.com")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        print("🔑 DEBUG: logging in…")
        server.login(EMAIL, PASSWORD)
        print("✉️ DEBUG: sending message…")
        server.send_message(msg)
    print("✅ DEBUG: Email sent!")
