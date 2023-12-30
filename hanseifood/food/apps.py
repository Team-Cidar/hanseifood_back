import os
import sys

from django.apps import AppConfig


class FoodsConfig(AppConfig):
    name = 'food'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # 이부분은 서버 가동중 준비되었을때 호출되는것이 아닌 app이 로드된 후에 즉시 호출하게됨.
        # 따라서 migrate 명령에서도 또한 app이 로드되고 model을 db에 migration하기 때문에 호출이 됨
        if os.environ.get('RUN_MAIN', None) != 'true' and 'runserver' in sys.argv:
            # 서버 실행 시 main, reload 두가지 프로세스가 뜸
            # 따라서 위의 조건문으로 main 프로세스로 서버가 실행될 때 단 한번만 실행될 코드들은 여기에 작성
            # 예를 들어 스케줄러를 시작하거나 스케줄러 job이 서버 실행되고 한번 호출이 되어야하면 여기에 job method import해서 호출하면 됨

            # 스케줄러 사용 시 아래 코드 주석 해제 하면 됨
            # from .core.schedulers import enroll_job as scheduler
            # scheduler.start()
            pass

        super().ready()
