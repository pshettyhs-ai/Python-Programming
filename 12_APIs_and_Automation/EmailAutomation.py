# =============================================================================
# EmailAutomation.py
# Author  : Pavan Shetty H S
# Date    : August 2024
# Topic   : Sending Emails Programmatically using smtplib
# =============================================================================
#
# Notes from Pavan:
# Getting this working took longer than expected, not because of Python
# syntax but because of Gmail's security settings. Regular password
# auth doesn't work anymore for SMTP -- needed to generate a Google
# "App Password" specifically for this, since 2-factor auth blocks
# plain password SMTP login. Spent an embarrassing amount of time
# debugging "authentication failed" before realizing this.
# =============================================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

print("=" * 50)
print("    EMAIL AUTOMATION DEMO")
print("=" * 50)

# ---------------------
# IMPORTANT: Never hardcode credentials in source code!
# ---------------------
print("\n[1] Credential handling -- lesson learned the hard way")
print("""
  I initially hardcoded my email and app password directly in this
  script during testing. Caught myself before committing it to git,
  but it was a close call. Now I ALWAYS use environment variables:

    SENDER_EMAIL = os.environ.get("EMAIL_ADDRESS")
    SENDER_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")

  And I added a .env pattern + .gitignore entry so secrets never get
  committed. This is now a non-negotiable habit for ANY project
  involving credentials, API keys, or tokens.
""")

SENDER_EMAIL = os.environ.get("EMAIL_ADDRESS", "your_email@gmail.com")
SENDER_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD", "your_app_password")

# ---------------------
# Basic plain text email
# ---------------------
print("\n[2] Composing a basic email (demo -- not actually sent without real credentials)")

def send_simple_email(to_email, subject, body):
    """Sends a basic plain-text email via Gmail's SMTP server."""
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()   # upgrade to encrypted connection -- REQUIRED
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"  Email sent successfully to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("  Authentication failed -- this is the error I hit constantly")
        print("  before switching to an App Password. Regular Gmail password")
        print("  does NOT work for SMTP login when 2FA is enabled.")
        return False
    except Exception as e:
        print(f"  Failed to send email: {e}")
        return False

print("  Function defined. Example call (commented to avoid actually sending):")
print("""
  send_simple_email(
      to_email="recipient@example.com",
      subject="Test from Python Learning Journey",
      body="This is an automated test email from my Python script."
  )
""")

# ---------------------
# HTML formatted email
# ---------------------
print("[3] HTML formatted email")

def send_html_email(to_email, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"  HTML email sent to {to_email}")
        return True
    except Exception as e:
        print(f"  Failed: {e}")
        return False

html_template = """
<html>
  <body>
    <h2 style="color: navy;">Weekly Progress Report</h2>
    <p>Hi there,</p>
    <p>This week I completed: <b>Module 12 - APIs and Automation</b></p>
    <p>Regards,<br>Pavan Shetty H S</p>
  </body>
</html>
"""
print("  HTML email function defined with a sample progress report template")

# ---------------------
# Sending email with an attachment
# ---------------------
print("\n[4] Email with file attachment")

def send_email_with_attachment(to_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    if os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            attachment = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        attachment["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(attachment)
    else:
        print(f"  Warning: attachment {attachment_path} not found, sending without it")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"  Email with attachment sent to {to_email}")
        return True
    except Exception as e:
        print(f"  Failed: {e}")
        return False

print("  Function defined -- I use this exact pattern in the Expense")
print("  Tracker project to email myself a monthly PDF report automatically.")

# ---------------------
# Practical use case: automated report sender
# ---------------------
print("\n[5] Practical use case I actually built")
print("""
  Combined this with the schedule library to send myself a weekly
  learning progress email every Sunday night automatically:

    import schedule

    def weekly_report():
        send_simple_email(
            "myself@gmail.com",
            "Weekly Python Progress",
            f"Completed modules this week: ..."
        )

    schedule.every().sunday.at("20:00").do(weekly_report)
    while True:
        schedule.run_pending()
        time.sleep(60)

  Haven't kept this running 24/7 (would need a server, not my laptop),
  but it works correctly whenever I run it during testing.
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 EmailAutomation.py
# =============================================================================
#
# ==================================================
#     EMAIL AUTOMATION DEMO
# ==================================================
#
# [1] Credential handling -- lesson learned the hard way
#
#   I initially hardcoded my email and app password directly in this
#   script during testing. Caught myself before committing it to git,
#   but it was a close call. Now I ALWAYS use environment variables:
#
#     SENDER_EMAIL = os.environ.get("EMAIL_ADDRESS")
#     SENDER_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")
#
#   And I added a .env pattern + .gitignore entry so secrets never get
#   committed. This is now a non-negotiable habit for ANY project
#   involving credentials, API keys, or tokens.
#
#
# [2] Composing a basic email (demo -- not actually sent without real credentials)
#   Function defined. Example call (commented to avoid actually sending):
#
#   send_simple_email(
#       to_email="recipient@example.com",
#       subject="Test from Python Learning Journey",
#       body="This is an automated test email from my Python script."
#   )
#
# [3] HTML formatted email
#   HTML email function defined with a sample progress report template
#
# [4] Email with file attachment
#   Function defined -- I use this exact pattern in the Expense
#   Tracker project to email myself a monthly PDF report automatically.
#
# [5] Practical use case I actually built
#
#   Combined this with the schedule library to send myself a weekly
#   learning progress email every Sunday night automatically:
#
#     import schedule
#
#     def weekly_report():
#         send_simple_email(
#             "myself@gmail.com",
#             "Weekly Python Progress",
#             f"Completed modules this week: ..."
#         )
#
#     schedule.every().sunday.at("20:00").do(weekly_report)
#     while True:
#         schedule.run_pending()
#         time.sleep(60)
#
#   Haven't kept this running 24/7 (would need a server, not my laptop),
#   but it works correctly whenever I run it during testing.
#
# ==================================================
#
# =============================================================================

