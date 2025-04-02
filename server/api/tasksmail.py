from celery import shared_task
from django.core.mail import send_mail
from dateutil import parser


@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    """Task to send an email using Celery."""
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )


def schedule_email(subject, message, from_email, recipient_list, send_time):
    """Schedule an email to be sent at a specific time."""
    utc_datetime = parser.parse(send_time)

    send_email_task.apply_async(
        args=[subject, message, from_email, recipient_list],
        eta=utc_datetime,  # Set the execution time to the parsed UTC datetime
    )
