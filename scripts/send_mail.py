import os
import smtplib
from email.mime.text import MIMEText


def send_email(subject: str, body: str) -> None:
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    email_from = os.environ.get("EMAIL_FROM")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    missing = []
    if not email_from:
        missing.append("EMAIL_FROM")
    if not email_password:
        missing.append("EMAIL_PASSWORD")
    if not email_to:
        missing.append("EMAIL_TO")

    if missing:
        raise ValueError(f"缺少必要環境變數: {', '.join(missing)}")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = email_to

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_from, email_password)
            server.send_message(msg)
        print(f"郵件已成功寄至 {email_to}")
    except Exception as e:
        raise RuntimeError(f"郵件發送失敗: {e}")
