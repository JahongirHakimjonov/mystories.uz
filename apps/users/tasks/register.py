import os

from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


@shared_task
def send_activation_email(email, activation_link):
    from_email = os.getenv("EMAIL_HOST_USER")
    subject = "Activate your account"
    message = f"Please click the link to activate your account: {activation_link}"
    send_mail(subject, message, from_email, [email])
