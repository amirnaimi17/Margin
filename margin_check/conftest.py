from decimal import Decimal

import pytest
from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker

from margin_check.choices import MARGIN_CLASS_CHOICES


@pytest.fixture
@freeze_time("2020-05-11 18:00")
def intraday_ci050_data_at_six_pm_yesterday(db):
    # intraday report of 2020-05-11 in CI050 at 18:00
    today = timezone.now()
    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("2882.2"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("988.1"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("788.3"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("908.9"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("123.4"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("8326.4"),
        report_date=today.date(),
        report_time=today.time(),
    )


@pytest.fixture
@freeze_time("2020-05-11 19:00")
def last_intraday_ci050_data_yesterday(db):
    # "last" intraday report of 2020-05-11 in CI050
    today = timezone.now()
    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("3212.2"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("837.1"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("8963.3"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("76687.9"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("821.4"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("8766.4"),
        report_date=today.date(),
        report_time=today.time(),
    )


@pytest.fixture
@freeze_time("2020-05-12 8:00")
def first_intraday_ci050_data_today(db):
    # "first" intraday report of 2020-05-12 in CI050
    today = timezone.now()
    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("3212.2"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("837.1"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("8963.3"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("76687.9"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("821.4"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("8766.4"),
        report_date=today.date(),
        report_time=today.time(),
    )


@pytest.fixture
@freeze_time("2020-05-12 9:00")
def second_intraday_ci050_data_today(db):
    # "second" intraday report of 2020-05-12 in CI050
    today = timezone.now()
    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("3133.9"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("137.1"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("2963.3"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("74687.9"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("811.4"),
        report_date=today.date(),
        report_time=today.time(),
    )

    baker.make_recipe(
        "margin_check.CI050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("8366.4"),
        report_date=today.date(),
        report_time=today.time(),
    )


@pytest.fixture
@freeze_time("2020-05-11")
def end_of_day_cc050_data(db):
    # end-of-day report of 2020-05-11 in CC050 table
    today = timezone.now()
    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("3212.2"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("837.1"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("8963.3"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("76687.9"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("821.4"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("8766.4"),
        report_date=today.date(),
    )


@pytest.fixture
@freeze_time("2020-05-11")
def end_of_day_cc050_corrupted_data(db):
    # end-of-day report of 2020-05-11 in CC050 table
    today = timezone.now()
    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("32.2"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 1",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("83.1"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("89.3"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 1",
        account="A2",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("766.9"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.SPAN,
        margin=Decimal("821.4"),
        report_date=today.date(),
    )

    baker.make_recipe(
        "margin_check.CC050",
        clearing_member="Bank 2",
        account="A1",
        margin_class=MARGIN_CLASS_CHOICES.IMSM,
        margin=Decimal("876.4"),
        report_date=today.date(),
    )
