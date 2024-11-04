import os

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_reset_email_task(email, frontend_url, uid, token):
    subject = "Password Reset Requested"
    message = render_to_string(
        "password_reset.html",
        {
            "frontend_url": frontend_url,
            "uid": uid,
            "token": token,
        },
    )
    send_mail(subject, message, os.getenv("EMAIL_HOST_USER"), [email])
