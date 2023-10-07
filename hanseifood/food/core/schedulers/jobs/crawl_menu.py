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
        crawler = MenuCrawler(driver_path=os.getenv("CHROME_DRIVER_PATH"))
        file_name = crawler.crawl()

        logger.info("Crawling job finished!")
        logger.info("Start saving datas to database")

        # parse
        path = 'datas/' + file_name + '.xlsx'

        # data: ParseObject = TempExcelParser.parse(path)  # new template parser
        data: ParseObject = ParseObject()
        data.keys = [
            '2023-10-10',
            '2023-10-11',
            '2023-10-12',
            '2023-10-13'
        ]
        data.students = {
            '2023-10-10': ['돼지고기김치찌개', '오징어링튀김/칠리s', '물만두/양념장', '깍두기', '건파래자반'],
            '2023-10-11': ['잔치국수', '셀프김가루주먹밥', '칠리새우', '단무지', '배추김치'],
            '2023-10-12': ['미역국', '간장불고기', '쫄면야채무침', '포기김치', '부추겉절이'],
            '2023-10-13': ['미니우동', '스팸김치볶음밥', '고구마고로케/케찹', '깍두기', '숙주나물무침']
        }
        data.employees = {
            '2023-10-10': ['돼지고기김치찌개', '오징어링튀김/칠리s', '물만두/양념장', '가지나물', '갓김치/건파래자반'],
            '2023-10-11': ['배추된장국', '고구마닭갈비', '눈꽃치즈계란찜', '열무된장나물', '포기김치/쌈무'],
            '2023-10-12': ['미역국', '간장불고기', '새송이메알조림', '쫄면야채무침', '포기김치/부추겉절이'],
            '2023-10-13': ['미니우동', '스팸김치볶음밥', '고구마고로케/케찹', '명엽채볶음', '깍두기/숙주나물무침']
        }
        data.additional = {
            '2023-10-10': ["돈까스 정식"],
            '2023-10-12': ["돈까스 정식"],
            '2023-10-13': ['돈까스 정식']
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

        try:
            _save_to_db(day_model, students[day], for_students=True, is_additional=False)
            _save_to_db(day_model, employees[day], for_students=False, is_additional=False)
            _save_to_db(day_model, additional[day], for_students=False, is_additional=True)
        except KeyError:
            # 메뉴가 student, employee, additinal 모두 존재하지 않는 날은 dict key에러가 나서 그냥 넘어가도록 처리
            pass


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
