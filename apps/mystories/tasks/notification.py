import logging

from celery import shared_task
from firebase_admin import messaging

from apps.mystories.models import Notification
from apps.users.models import ActiveSessions, User

logger = logging.getLogger(__name__)


def send_fcm_notification(notification, fcm_tokens):
    """
    Helper function to send FCM notification to a list of tokens.
    """
    for fcm_token in fcm_tokens:
        if fcm_token:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification.title,
                    body=notification.message,
                    image=(
                        notification.banner.url
                        if notification.banner and hasattr(notification.banner, "url")
                        else None
                    ),
                ),
                token=fcm_token,
            )
            messaging.send(message)


@shared_task
def send_notification_task(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        fcm_tokens = ActiveSessions.objects.filter(
            user=notification.user, is_active=True, fcm_token__isnull=False
        ).values_list("fcm_token", flat=True)
        send_fcm_notification(notification, fcm_tokens)
        notification.is_send = True
        notification.save()
        logger.info(f"Notification sent to user {notification.user.id}")
    except Notification.DoesNotExist:
        logger.error(f"Notification with id {notification_id} does not exist")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")


@shared_task
def send_notification_to_all_task(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        users = User.objects.all()
        for user in users:
            fcm_tokens = ActiveSessions.objects.filter(
                user=user, is_active=True, fcm_token__isnull=False
            ).values_list("fcm_token", flat=True)
            send_fcm_notification(notification, fcm_tokens)
        notification.is_send = True
        notification.save()
        logger.info("Notification sent to all users")
    except Notification.DoesNotExist:
        logger.error(f"Notification with id {notification_id} does not exist")
    except Exception as e:
        logger.error(f"Error sending notifications to all users: {e}")
