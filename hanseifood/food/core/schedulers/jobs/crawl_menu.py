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
            '2023-09-18',
            '2023-09-19',
            '2023-09-20',
            '2023-09-21',
            '2023-09-22'
        ]
        data.students = {
            '2023-09-18': ['마파두부덮밥', '황태부추국', '돈채피망볶음', '꽃빵연유튀김', '포기김치'],
            '2023-09-19': ['호박새우젓국', '닭볶음탕', '맛살겨자냉채', '열무된장나물', '포기김치'],
            '2023-09-20': ['유부김칫국', '숯불맛돈불고기', '떡볶이', '콩나물파채무침', '열무김치'],
            '2023-09-21': ['육개장', '닭가슴살냉채', '순대볶음', '무들깨나물', '포기김치'],
            '2023-09-22': ['김치볶음밥', '미니잔치국수', '산적구이', '고구마순볶음', '총각김치']
        }
        data.employees = {
            '2023-09-18': ['마파두부덮밥', '황태부추국', '돈채피망볶음', '꽃빵연유튀김', '포기김치', '고구마조림'],
            '2023-09-19': ['호박새우젓국', '닭볶음탕', '맛살겨자냉채', '열무된장나물', '포기김치', '탕평채'],
            '2023-09-20': ['유부김칫국', '숯불맛돈불고기', '떡볶이', '콩나물파채무침', '열무김치', '쌈무'],
            '2023-09-21': ['육개장', '닭가슴살냉채', '순대볶음', '무들깨나물', '포기김치', '건파래자반'],
            '2023-09-22': ['김치볶음밥', '미니잔치국수', '산적구이', '고구마순볶음', '총각김치', '양배추샐러드']
        }
        data.additional = {
            '2023-09-18': ['백미밥', '돈까스&소스', '크림스프', '양배추샐러드&드레싱', '단무지', '배추김치'],
            '2023-09-19': ['백미밥', '돈까스&소스', '크림스프', '양배추샐러드&드레싱', '단무지', '배추김치'],
            '2023-09-20': ['우동국', '치킨마요덮밥', '떡볶이', '단무지', '배추김치'],
            '2023-09-21': ['백미밥', '돈까스&소스', '크림스프', '양배추샐러드&드레싱', '단무지', '배추김치'],
            '2023-09-22': ['백미밥', '돈까스&소스', '크림스프', '양배추샐러드&드레싱', '단무지', '배추김치'],
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
