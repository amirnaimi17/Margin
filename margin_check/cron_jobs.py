import logging

from django_cron import CronJobBase, Schedule

from margin_check.tasks import (
    check_differences_of_cc050_and_ci050_first_intraday,
    check_differences_of_cc050_and_ci050_last_intraday,
)

logger = logging.getLogger(__name__)


class MarginCheckCronJob(CronJobBase):
    RUN_AT_TIMES = ["23:50"]

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = "margin_check.cron_jobs"

    def do(self):
        check_differences_of_cc050_and_ci050_first_intraday.delay()
        check_differences_of_cc050_and_ci050_last_intraday.delay()
        logger.info("Cron has been done successfully.")
