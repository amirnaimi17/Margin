import contextlib
import socket
from datetime import timedelta
from smtplib import SMTPException

from celery import current_task
from django.conf import settings
from django.utils import timezone

from margin.celery import app
from margin_check.models import CI050
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
def check_differences_of_ci050(*args, **kwargs):
    now = timezone.now()
    today_queryset = (
        CI050.objects.filter(report_date=now.date())
        .order_by("report_time")
        .distinct("report_time", "clearing_member", "account", "margin_class")
        .values("clearing_member", "account", "margin_class", "margin")
    )

    yesterday = timezone.now() - timedelta(days=1)
    yesterday_queryset = (
        CI050.objects.filter(report_date=yesterday.date())
        .order_by("-report_time")
        .distinct("report_time", "clearing_member", "account", "margin_class")
        .values("clearing_member", "account", "margin_class", "margin")
    )

    difference = today_queryset.difference(yesterday_queryset)
    if difference:
        send_email.delay(
            emails=settings.CHECK_RECIPIENTS,
            context={
                "difference": [],
            },
            template_name="check_differences.html",
            subject="Check the differences",
        )
