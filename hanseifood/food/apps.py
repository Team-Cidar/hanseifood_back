import logging
import os

from django.apps import AppConfig


class FoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'food'

    def ready(self):
        super().ready()

        if os.environ.get('RUN_MAIN', None) != 'true':
            # 서버 실행 시 main, reload 두가지 프로세스가 뜨는데 아래부분은 스케줄러 등록부분이라
            # 한번만 등록해줘야함. 따라서 위의 조건문으로 main 프로세스일 때만 등록되어 한번만 등록되도록함
            # 이거 없으면 스케줄러 자꾸 두번씩 호출됨
            from . import operator
            operator.start()

            # do scheduled job once server started
            from .utils.schedulers.crawling_job import save_menu_scheduler_job
            save_menu_scheduler_job()
