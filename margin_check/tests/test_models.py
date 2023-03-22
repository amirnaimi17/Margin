from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time

from margin_check.models import CC050, CI050


class TestCI050:
    @freeze_time("2020-05-12 23:50")
    def test_get_distinct_data_by_report_date_for_today(
        self,
        intraday_ci050_data_at_six_pm_yesterday,
        last_intraday_ci050_data_yesterday,
        first_intraday_ci050_data_today,
        second_intraday_ci050_data_today,
    ):
        # Total records in table
        assert CI050.objects.count() == 24

        today = timezone.now()
        today_queryset = CI050.get_distinct_data_by_report_date(
            report_date=today.date()
        )
        # There are 12 records for today but only 6 records are the earliest
        assert len(today_queryset) == 6

        yesterday = today - timedelta(days=1)
        yesterday_queryset = CI050.get_distinct_data_by_report_date(
            report_date=yesterday, order_by="DESC"
        )
        # There are 12 records for yesterday but only 6 records are the latest
        assert len(yesterday_queryset) == 6


class TestCC050:
    @freeze_time("2020-05-11")
    def test_get_distinct_data_by_report_date_for_today(self, end_of_day_cc050_data):
        # Total records in table
        assert CC050.objects.count() == 6

        today = timezone.now()
        today_queryset = CC050.get_distinct_data_by_report_date(
            report_date=today.date()
        )
        # There are 12 records for today but only 6 records are the earliest
        assert len(today_queryset) == 6
