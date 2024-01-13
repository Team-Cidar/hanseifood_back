import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

logger = logging.getLogger(__name__)


# apps.py에서 scheduler 등록 (실행)
def start():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    try:
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        register_events(scheduler)
        scheduler.start()

        # insert jobs here
    except Exception as e:
        logger.error(e)
