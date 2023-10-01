import os.path
from datetime import datetime
import logging

from ...utils.date_utils import get_dates_in_this_week
from ..modules.crawler import MenuCrawler
from ..modules.temp_excel_parser import TempExcelParser
from ....repositories.day_repository import DayRepository
from ....repositories.daymeal_repository import DayMealRepository
from ....repositories.meal_repository import MealRepository
from ..modules.objs.parse_obj import ParseObject

logger = logging.getLogger(__name__)
__all__ = ['get_and_save_menus']  # ~~ import * 로 불러오면 이 함수만 import 됨

day_repository = DayRepository()
meal_repository = MealRepository()
day_meal_repository = DayMealRepository()


# scheduler에 등록할 함수
def get_and_save_menus():
    try:
        logger.info('Execute scheduled job / get_menu_data_schedule')
        # clear all datas
        # day_repository.clearAll()
        # meal_repository.clearAll()
        # day_meal_repository.clearAll()

        # check if already did crawling
        for date in get_dates_in_this_week(end=6):
            date_str = date.strftime('%Y%m%d')
            if os.path.exists(f'datas/{date_str}.xlsx'):
                logger.info("This week's menu data is already saved")
                return

        # crawling
        # crawler = MenuCrawler(driver_path='/app/src/hanseifood/drivers/chromedriver')
        # crawler = MenuCrawler('food/chromedriver')  # for test
        crawler = MenuCrawler(driver_path=os.getenv("CHROME_DRIVER_PATH", '/app/src/hanseifood/drivers/chromedriver'))
        file_name = crawler.crawl()

        logger.info("Crawling job finished!")
        logger.info("Start saving datas to database")

        # parse
        path = 'datas/' + file_name + '.xlsx'
        # path = 'datas/test2.xlsx'    # for test

        # data: ParseObject = TempExcelParser.parse(path)  # new template parser
        data: ParseObject = ParseObject()
        data.keys = [
            '2023-10-04',
            '2023-10-05',
            '2023-10-06'
        ]
        data.students = {
            '2023-10-04': ['미소장국', '참치마요덮밥', '미니핫도그/케찹', '단무지', '배추김치'],
            '2023-10-05': ['사골떡국', '김치제육볶음', '만두튀김', '콩나물무침', '깍두기'],
            '2023-10-06': ['부대찌개', '치킨가라아게', '옥수수콘샐러드', '요구르트', '깍두기']
        }
        data.employees = {
            '2023-10-04': ['닭곰탕', '한식잡채', '매콤새송이두부조림', '모닝빵&딸기잼', '포기김치', '미역줄기들깨볶음'],
            '2023-10-05': ['사골떡국', '김치제육볶음', '만두튀김', '콩나물무침', '열무김치', '건파래자반'],
            '2023-10-06': ['부대찌개', '치킨가라아게', '옥수수콘샐러드', '요구르트', '깍두기', '감자조림']
        }
        data.additional = {
            '2023-10-05': ["돈까스 정식"],
            '2023-10-06': ["돈까스 정식"]
        }
        _save_data_temp(data)

        logger.info("save finished!")
    except Exception as e:
        logger.error(e)


def _save_data_temp(data: ParseObject):
    students: dict = data.students
    employees: dict = data.employees
    additional: dict = data.additional

    for day in data.keys:
        date = datetime.strptime(day, "%Y-%m-%d")

        day_model = day_repository.findByDate(date)
        if day_model.exists():
            logger.info(f'{day} is already exists')
            continue
        day_model = day_repository.save(date)

        _save_to_db(day_model, students[day], for_students=True, is_additional=False)
        _save_to_db(day_model, employees[day], for_students=False, is_additional=False)
        _save_to_db(day_model, additional[day], for_students=False, is_additional=True)


def _save_to_db(day_model, datas: list, for_students: bool, is_additional: bool):
    # save meals
    for menu in datas:
        menu_model = meal_repository.findByMenuName(menu)
        if not menu_model.exists():
            menu_model = meal_repository.save(menu)
        else:
            menu_model = menu_model[0]

        day_meal_repository.save(day_id=day_model, meal_id=menu_model, for_student=for_students,
                                 is_additional=is_additional)
