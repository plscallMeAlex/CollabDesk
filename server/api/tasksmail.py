# api/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from dateutil import parser


@shared_task
def send_scheduled_email(subject, message, from_email, recipient_list, task_id=None):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )


def schedule_email(
    subject, message, from_email, recipient_list, scheduled_time_str, task_id
):
    utc_datetime = parser.parse(scheduled_time_str)

    # Include a task_id in kwargs that can be used for identification
    task = send_scheduled_email.apply_async(
        args=[subject, message, from_email, recipient_list],
        eta=utc_datetime,
        kwargs={"task_id": task_id},
    )

    # Return the task ID so it can be stored or used for updates
    return task.id


def update_scheduled_email(
    task_id,
    subject=None,
    message=None,
    from_email=None,
    recipient_list=None,
    new_scheduled_time_str=None,
):
    from celery.app.control import revoke
    from celery.result import AsyncResult

    # Check if the task exists
    result = AsyncResult(task_id)
    task_exists = result.state != "PENDING" or result.task_id is not None

    if task_exists:
        # Revoke the existing task
        revoke(task_id, terminate=True)

    # Schedule a new task with updated information
    utc_datetime = (
        parser.parse(new_scheduled_time_str) if new_scheduled_time_str else None
    )

    # Use the provided task_id directly
    new_task = send_scheduled_email.apply_async(
        args=[subject, message, from_email, recipient_list],
        eta=utc_datetime,
        kwargs={"task_id": task_id},
    )

    return new_task.id, task_exists  # Return whether the original task existed


def cancel_scheduled_email(task_id):
    from celery.app.control import revoke
    from celery.result import AsyncResult

    # Check if the task exists
    result = AsyncResult(task_id)
    task_exists = result.state != "PENDING" or result.task_id is not None

    if task_exists:
        # Revoke the existing task
        revoke(task_id, terminate=True)

    return task_exists  # Return whether the original task existed
