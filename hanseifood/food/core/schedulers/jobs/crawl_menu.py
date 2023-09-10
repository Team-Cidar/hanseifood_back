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
        crawler = MenuCrawler('/app/src/hanseifood/drivers/chromedriver')
        # crawler = MenuCrawler('food/chromedriver')  # for test
        file_name = crawler.crawl()

        logger.info("Crawling job finished!")
        logger.info("Start saving datas to database")

        # parse
        path = 'datas/' + file_name + '.xlsx'
        # path = 'datas/test2.xlsx'    # for test

        # data: ParseObject = TempExcelParser.parse(path)  # new template parser
        data: ParseObject = ParseObject()
        data.keys = [
            '2023-09-11',
            '2023-09-12',
            '2023-09-13',
            '2023-09-14',
            '2023-09-15'
        ]
        data.students = {
            '2023-09-11': ['무들깨국', '매콤콩나물불고기', '찐만두&양념장', '건새우호박볶음', '포기김치'],
            '2023-09-12': ['맑은콩나물국', '참치김치볶음', '온두부', '미역줄기볶음', '깍두기'],
            '2023-09-13': ['짜장덮밥/계란실파국', '소세지야채볶음', '만두탕수', '단무지', '포기김치'],
            '2023-09-14': ['순두부짬뽕탕', '생선까스/타르s', '청경채당면볶음', '얼갈이겉절이', '포기김치'],
            '2023-09-15': ['돈육김치찌개', '닭살카레볶음', '야채계란찜', '가지나물', '깍두기']
        }
        data.employees = {
            '2023-09-11': ['무들깨국', '매콤콩나물불고기', '찐만두&양념장', '건새우호박볶음', '포기김치', '채썬쌈무'],
            '2023-09-12': ['맑은콩나물국', '참치김치볶음', '온두부', '미역줄기볶음', '깍두기', '녹차', '열무김치'],
            '2023-09-13': ['짜장덮밥/계란실파국', '소세지야채볶음', '만두탕수', '단무지', '포기김치', '숙주나물'],
            '2023-09-14': ['순두부짬뽕탕', '생선까스/타르s', '청경채당면볶음', '얼갈이겉절이', '포기김치', '요쿠르트'],
            '2023-09-15': ['돈육김치찌개', '닭살카레볶음', '야채계란찜', '가지나물', '깍두기', '도시락김']
        }
        data.additional = {
            '2023-09-11': ['백미밥', '돈까스&소스', '크림스프', '모닝빵&딸기잼', '단무지', '김치'],
            '2023-09-12': ['백미밥', '돈까스&소스', '크림스프', '모닝빵&딸기잼', '단무지', '김치'],
            '2023-09-13': ['백미밥', '돈까스&소스', '크림스프', '모닝빵&딸기잼', '단무지', '김치'],
            '2023-09-14': ['백미밥', '돈까스&소스', '크림스프', '모닝빵&딸기잼', '단무지', '김치'],
            '2023-09-15': ['백미밥', '돈까스&소스', '크림스프', '모닝빵&딸기잼', '단무지', '김치']
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
