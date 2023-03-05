import logging

from django_cron import CronJobBase, Schedule

from margin_check.tasks import check_differences_of_ci050

logger = logging.getLogger(__name__)


class MarginCheckCronJob(CronJobBase):
    RUN_AT_TIMES = ["23:50"]

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = "margin_heck.cron_jobs"

    def do(self):
        print("it is started")
        check_differences_of_ci050.delay()
        logger.info("Cron has been done successfully.")
