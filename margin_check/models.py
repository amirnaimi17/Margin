from django.db import models
from django.utils.translation import gettext_lazy as _

from margin_check.choices import MARGIN_CLASS_CHOICES


class BaseMarginReport(models.Model):
    clearing_member = models.CharField(
        max_length=200, verbose_name=_("clearing member"), db_index=True
    )
    account = models.CharField(max_length=200, verbose_name=_("account"), db_index=True)
    margin_class = models.CharField(
        max_length=10,
        verbose_name=_("margin type"),
        choices=MARGIN_CLASS_CHOICES.choices,
        db_index=True,
    )
    margin = models.DecimalField(_("margin"), decimal_places=1, max_digits=6)
    report_date = models.DateField(_("report date"), db_index=True)


class CC050(BaseMarginReport):
    def __str__(self):
        return f"{self.clearing_member}-{self.account}-{self.margin_class}-{self.report_date}"

    @classmethod
    def get_distinct_data_by_report_date(
        cls,
        report_date=None,
    ):
        return (
            cls.objects.filter(report_date=report_date)
            .distinct("clearing_member", "account", "margin_class")
            .values("clearing_member", "account", "margin_class", "margin")
        )


class CI050(BaseMarginReport):
    report_time = models.TimeField(_("report time"))

    def __str__(self):
        return f"{self.clearing_member}-{self.account}-{self.margin_class}-{self.report_time}"

    @classmethod
    def get_distinct_data_by_report_date(cls, report_date=None, order_by="ASC"):
        queryset = (
            cls.objects.filter(report_date=report_date)
            .distinct("clearing_member", "account", "margin_class")
            .values("clearing_member", "account", "margin_class", "margin")
        )

        if order_by == "ASC":
            queryset = queryset.order_by(
                "clearing_member", "account", "margin_class", "report_time"
            )
        else:
            queryset = queryset.order_by(
                "clearing_member", "account", "margin_class", "-report_time"
            )

        return queryset
