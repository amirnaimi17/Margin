import contextlib
import socket
from datetime import timedelta
from smtplib import SMTPException

from celery import current_task
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from margin.celery import app
from margin_check.models import CC050, CI050
from margin_check.utils import TemplateEmail


@contextlib.contextmanager
def retry_on_smtp_errors():
    try:
        yield
    except (socket.error, SMTPException) as e:
        current_task.retry(exc=e, countdown=current_task.request.retries * 2)


@app.task
def send_email(*args, **kwargs):
    """Generate email and send."""
    emails = kwargs.get("emails")
    context = kwargs.get(
        "context",
    )
    template_name = kwargs.get("template_name")
    subject = kwargs.get("subject")
    for email_address in emails:
        mail = TemplateEmail(
            subject=subject,
            from_email=settings.ADMIN_EMAIL,
            to=[email_address],
            template_name=template_name,
            context=context,
        )
        with retry_on_smtp_errors():
            mail.send()


@app.task
def check_differences_of_cc050_and_ci050_first_intraday(*args, **kwargs):
    """Check, if the end-of-day values of the previous day are the same as the first intraday values."""
    # The first intraday values of today
    now = timezone.now()
    ci050_queryset = CI050.get_distinct_data_by_report_date(report_date=now.date())

    if not ci050_queryset:
        raise ValidationError(f"No record has been inserted for today {now} in CI050")

    # The end-of-day values of yesterday
    yesterday = now - timedelta(days=1)
    cc050_queryset = CC050.get_distinct_data_by_report_date(
        report_date=yesterday.date()
    )

    if not cc050_queryset:
        raise ValidationError(f"No record inserted yesterday {yesterday} in CC050")

    # if there is a difference between both table records, inform Recipients by email.
    differences = cc050_queryset.difference(ci050_queryset)
    if differences:
        send_email.delay(
            emails=settings.CHECK_RECIPIENTS,
            context={
                "differences": [difference for difference in differences.all()],
                "date": now.date(),
            },
            template_name="check_differences.html",
            subject="Differences of first intraday values",
        )


@app.task
def check_differences_of_cc050_and_ci050_last_intraday(*args, **kwargs):
    """
    Check, if the end-of-day values are the same as the last intraday values.

    It runs every day, a few minutes before midnight to evaluate the records of both tables CI050 and CC050.
    For example: this will run at 23:50 on 2020-05-05.
    """
    # The last intraday values of today
    now = timezone.now()
    ci050_queryset = CI050.get_distinct_data_by_report_date(
        report_date=now.date(), order_by="DESC"
    )

    if not ci050_queryset:
        raise ValidationError(f"No record inserted today {now} in CI050")

    # The end-of-day values of today
    cc050_queryset = CC050.get_distinct_data_by_report_date(report_date=now.date())

    if not cc050_queryset:
        raise ValidationError(f"No record inserted today {now} in CC050")

    # if there is a difference between both table records, inform Recipients by email.
    differences = cc050_queryset.difference(ci050_queryset)
    if differences:
        send_email.delay(
            emails=settings.CHECK_RECIPIENTS,
            context={
                "differences": [difference for difference in differences.all()],
                "date": now.date(),
            },
            template_name="check_differences.html",
            subject="Differences of last intraday values",
        )
