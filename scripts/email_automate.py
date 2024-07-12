import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv
import schedule
import time

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

# Loading the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Reading environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")

def send_email(subject, receiver_email, name, attachment_path):
    # Creating the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Your Company Name", sender_email))
    msg["To"] = receiver_email

    msg.set_content(
        f"""\
        Hi {name},
        I hope you are well.
        Please find attached the daily sales report PDF.
        Best regards,
        John Doe
        """
    )

    # Attaching PDF file
    with open(attachment_path, "rb") as file:
        file_data = file.read()
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file.name)

    # Sending email
    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.send_message(msg)

def schedule_email(subject, receiver_email, name, attachment_path, scheduled_time):
    def job():
        send_email(subject, receiver_email, name, attachment_path)

    # Scheduling job
    schedule.every().day.at(scheduled_time).do(job)

    # Infinite loop to keep the script running until the scheduled time
    while True:
        schedule.run_pending()
        time.sleep(1)