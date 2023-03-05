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
    margin = models.DecimalField(_("margin"), decimal_places=2, max_digits=5)
    report_date = models.DateField(_("report date"), db_index=True)


class CC050(BaseMarginReport):
    def __str__(self):
        return f"{self.clearing_member}-{self.account}-{self.margin_class}-{self.report_date}"


class CI050(BaseMarginReport):
    report_time = models.TimeField(_("report time"))

    def __str__(self):
        return f"{self.clearing_member}-{self.account}-{self.margin_class}-{self.report_time}"
