import datetime
from datetime import timedelta

import pytest
from django.conf import settings
from django.core import mail
from django.core.exceptions import ValidationError
from django.utils import timezone
from freezegun import freeze_time

from margin_check.models import CC050, CI050
from margin_check.tasks import (
    check_differences_of_cc050_and_ci050_first_intraday,
    check_differences_of_cc050_and_ci050_last_intraday,
)


@freeze_time("2020-05-12 23:50")
def test_no_differences_of_cc050_and_ci050_first_intraday(
    first_intraday_ci050_data_today,
    second_intraday_ci050_data_today,
    end_of_day_cc050_data,
):
    # total records in the table
    assert CI050.objects.count() == 12
    assert set(CI050.objects.all().values_list("report_time", flat=True)) == {
        datetime.time(8, 0),
        datetime.time(9, 0),
    }

    assert CC050.objects.count() == 6

    now = timezone.now()
    ci050_queryset = CI050.get_distinct_data_by_report_date(report_date=now.date())
    assert len(ci050_queryset) == 6

    yesterday = now - timedelta(days=1)
    cc050_queryset = CC050.get_distinct_data_by_report_date(
        report_date=yesterday.date()
    )
    assert len(cc050_queryset) == 6

    assert list(ci050_queryset.values_list("margin", flat=True)) == list(
        cc050_queryset.values_list("margin", flat=True)
    )

    check_differences_of_cc050_and_ci050_first_intraday.delay()
    assert len(mail.outbox) == 0


@freeze_time("2020-05-12 23:50")
def test_differences_between_cc050_and_ci050_first_intraday(
    second_intraday_ci050_data_today, end_of_day_cc050_data
):
    # In this test we have removed the first intraday values of today
    # so there will be some records in CI050 but not the first intraday values
    assert CI050.objects.count() == 6
    assert set(CI050.objects.all().values_list("report_time", flat=True)) == {
        datetime.time(9, 0)
    }

    assert CC050.objects.count() == 6

    now = timezone.now()
    ci050_queryset = CI050.get_distinct_data_by_report_date(report_date=now.date())
    assert len(ci050_queryset) == 6

    yesterday = now - timedelta(days=1)
    cc050_queryset = CC050.get_distinct_data_by_report_date(
        report_date=yesterday.date()
    )
    assert len(cc050_queryset) == 6

    assert list(ci050_queryset.values_list("margin", flat=True)) != list(
        cc050_queryset.values_list("margin", flat=True)
    )

    # in this test, data in cc050 is fine but ci050 does not have correct data
    check_differences_of_cc050_and_ci050_first_intraday.delay()
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == settings.CHECK_RECIPIENTS
    # margins in cc050 is in the email body
    assert "3212.2" in email.body
    assert "8963.3" in email.body
    assert "76687.9" in email.body
    assert "837.1" in email.body
    assert "8766.4" in email.body


@freeze_time("2020-05-12 23:50")
def test_differences_between_cc050_and_ci050_first_intraday_2(
    first_intraday_ci050_data_today, end_of_day_cc050_corrupted_data
):
    # In this test we have removed the first intraday values of today
    # so there will be some records in CI050 but not the first intraday values
    assert CI050.objects.count() == 6
    assert set(CI050.objects.all().values_list("report_time", flat=True)) == {
        datetime.time(8, 0)
    }

    assert CC050.objects.count() == 6

    now = timezone.now()
    ci050_queryset = CI050.get_distinct_data_by_report_date(report_date=now.date())
    assert len(ci050_queryset) == 6

    yesterday = now - timedelta(days=1)
    cc050_queryset = CC050.get_distinct_data_by_report_date(
        report_date=yesterday.date()
    )
    assert len(cc050_queryset) == 6

    assert list(ci050_queryset.values_list("margin", flat=True)) != list(
        cc050_queryset.values_list("margin", flat=True)
    )

    # in this test, data in cc050 does not have correct data but ci050 is fine
    check_differences_of_cc050_and_ci050_first_intraday.delay()
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == settings.CHECK_RECIPIENTS
    # margins in cc050 is in the email body
    assert "32.2" in email.body
    assert "89.3" in email.body
    assert "766.9" in email.body
    assert "83.1" in email.body
    assert "876.4" in email.body


@freeze_time("2020-05-11 23:50")
def test_no_differences_of_cc050_and_ci050_last_intraday(
    intraday_ci050_data_at_six_pm_yesterday,
    last_intraday_ci050_data_yesterday,
    end_of_day_cc050_data,
):
    # total records in the table
    assert CI050.objects.count() == 12
    assert set(CI050.objects.all().values_list("report_time", flat=True)) == {
        datetime.time(19, 0),
        datetime.time(18, 0),
    }

    assert CC050.objects.count() == 6

    now = timezone.now()
    ci050_queryset = CI050.get_distinct_data_by_report_date(
        report_date=now.date(), order_by="DESC"
    )
    assert len(ci050_queryset) == 6

    cc050_queryset = CC050.get_distinct_data_by_report_date(report_date=now.date())
    assert len(cc050_queryset) == 6

    assert list(ci050_queryset.values_list("margin", flat=True)) == list(
        cc050_queryset.values_list("margin", flat=True)
    )

    check_differences_of_cc050_and_ci050_last_intraday.delay()
    assert len(mail.outbox) == 0


@freeze_time("2020-05-11 23:50")
def test_differences_of_cc050_and_ci050_last_intraday(
    intraday_ci050_data_at_six_pm_yesterday, end_of_day_cc050_data
):
    # total records in the table
    assert CI050.objects.count() == 6
    assert set(CI050.objects.all().values_list("report_time", flat=True)) == {
        datetime.time(18, 0)
    }

    assert CC050.objects.count() == 6

    now = timezone.now()
    ci050_queryset = CI050.get_distinct_data_by_report_date(
        report_date=now.date(), order_by="DESC"
    )
    assert len(ci050_queryset) == 6

    cc050_queryset = CC050.get_distinct_data_by_report_date(report_date=now.date())
    assert len(cc050_queryset) == 6

    assert list(ci050_queryset.values_list("margin", flat=True)) != list(
        cc050_queryset.values_list("margin", flat=True)
    )

    check_differences_of_cc050_and_ci050_last_intraday.delay()
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == settings.CHECK_RECIPIENTS


@freeze_time("2020-05-12 23:50")
def test_raise_in_ci050(
    end_of_day_cc050_data,
):
    # There is no data in the table for today
    assert not CI050.objects.count()
    now = timezone.now().date()
    with pytest.raises(ValidationError) as e:
        check_differences_of_cc050_and_ci050_first_intraday()
        assert e.value.messages == [
            f"No record has been inserted for today {now} in CI050"
        ]


@freeze_time("2020-05-12 23:50")
def test_raise_in_cc050(
    first_intraday_ci050_data_today,
    second_intraday_ci050_data_today,
):
    # Total records of the table that contains today's records
    assert CI050.objects.count() == 12
    assert not CC050.objects.count()
    yesterday = timezone.now().date() - timedelta(days=1)
    with pytest.raises(ValidationError) as e:
        check_differences_of_cc050_and_ci050_first_intraday()
        assert e.value.messages == [
            f"No record inserted yesterday {yesterday} in CC050"
        ]


@freeze_time("2020-05-12 23:50")
def test_raise_in_ci050_last_intraday(
    end_of_day_cc050_data,
):
    # There is no data in the table for today
    assert not CI050.objects.count()
    assert CC050.objects.count() == 6
    now = timezone.now().date()
    with pytest.raises(ValidationError) as e:
        check_differences_of_cc050_and_ci050_last_intraday()
        assert e.value.messages == [
            f"No record has been inserted for today {now} in CI050"
        ]


@freeze_time("2020-05-12 23:50")
def test_raise_in_cc050_last_intraday(
    first_intraday_ci050_data_today,
    second_intraday_ci050_data_today,
):
    # Total records of the table that contains today's records
    assert CI050.objects.count() == 12
    assert not CC050.objects.count()
    yesterday = timezone.now().date() - timedelta(days=1)
    with pytest.raises(ValidationError) as e:
        check_differences_of_cc050_and_ci050_last_intraday()
        assert e.value.messages == [
            f"No record inserted yesterday {yesterday} in CC050"
        ]
