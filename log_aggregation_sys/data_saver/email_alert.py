from django.conf import settings
from django.core.mail import send_mail


def send_email_alert(instance) -> None:

    message = f"Logs aggregation system detected error data log" \
              f" associated with" \
              f" {instance.__class__.__name__} at {instance.created_at}"

    send_mail(
        subject="Logs aggregation system error",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.ALERT_EMAIL_ADDRESS],
    )
