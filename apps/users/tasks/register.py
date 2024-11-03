import os

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


@shared_task
def send_activation_email(email, activation_link):
    from_email = os.getenv("EMAIL_HOST_USER")
    subject = "Activate your account"

    html_message = render_to_string(
        "activate.html",
        {"activation_link": activation_link},
    )
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, [email], html_message=html_message)
