import os
import sys

from django.apps import AppConfig


class FoodsConfig(AppConfig):
    name = 'food'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # 이부분은 서버 가동중 준비되었을때 호출되는것이 아닌 app이 로드된 후에 즉시 호출하게됨.
        # 따라서 migrate 명령에서도 또한 app이 로드되고 model을 db에 migration하기 때문에 호출이 됨
        # scheduler 작동 코드는 따로 분리하거나 추가적인 조건문을 붙여야할 필요가 있어보임
        super().ready()
        if os.environ.get('RUN_MAIN', None) == 'true' and 'runserver' in sys.argv:
            # 서버 실행 시 main, reload 두가지 프로세스가 뜨는데 아래부분은 스케줄러 등록부분이라
            # 한번만 등록해줘야함. 따라서 위의 조건문으로 main 프로세스일 때만 등록되어 한번만 등록되도록함
            # 이거 없으면 스케줄러 자꾸 두번씩 호출됨
            from .core.schedulers import enroll_job as scheduler
            scheduler.start()

            # do scheduled job once server started
            from .core.schedulers.jobs.crawl_menu import get_and_save_menus
            get_and_save_menus()
