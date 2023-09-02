from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from apscheduler.triggers.cron import CronTrigger

from .jobs.crawl_menu import get_and_save_menus


# apps.py에서 scheduler 등록 (실행)
def start():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    try:
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        register_events(scheduler)
        scheduler.start()

        scheduler.add_job(
            get_and_save_menus,
            trigger=CronTrigger(
                day_of_week='mon', hour=8
            ),
            id='get_menu',
            max_instances=1,
            replace_existing=True,
            coalesce=True,  # 동일 스케쥴 시간에 여러 인스턴스가 있다면 한번만 실행되도록 (충돌 방지)
            misfire_grace_time=1000
            # sqlite는 단일 쓰레드 지원으로 scheduler thread, main thread에서 db connection을 여는 코드가 동시에 존재할 수 없음 => db 연결이 lock됨.
            # 이 옵션은 따라서 이렇게 여러 곳에서 db connection이 생길 경우에 적용하는 옵션으로 정확히는 작업이 예정된 시간을 지나친 후에도 등록해둔 메서드가 실행되지 않은 경우 특정 시간동안 기다리도록 함.
            # connection이 진행중이라면 해당 시간(초)만큼 기다렸다가 실행할 수 있도록 함
        )
    except Exception as e:
        print(e)
        print('exception!!')
