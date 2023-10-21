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
            '2023-10-23',
            '2023-10-24',
            '2023-10-25',
            '2023-10-26',
            '2023-10-27'
        ]
        data.students = {
            '2023-10-23': ['뼈없는감자탕', '갈비만두/양념장', '두부조림', '진미채볼어묵무침', '배추김치'],
            '2023-10-24': ['조랑떡계란국', '오지어제육볶음', '버섯잡채', '건파래자반', '배추김치'],
            '2023-10-25': ['콩나물김칫국', '추가백미밥', '로제크림파스타', '알감자버터구이', '미니핫도그/케찹', '깍두기'],
            '2023-10-26': ['근대된장국', '지코바닭갈비', '비빔막국수', '야채스틱/쌈장', '배추김치'],
            '2023-10-27': ['설렁탕/소면', '오징어초무침', '간장떡볶이', '요구르트', '깍두기']
        }
        data.employees = {
            '2023-10-23': ['뼈없는감자탕', '갈비만두/양념장', '두부조림', '진미채볼어묵무침', '포기김치/야채샐러드'],
            '2023-10-24': ['조랑떡계란국', '오지어제육볶음', '버섯잡채', '알배기배추쌈*쌈잠', '포기김치/사각어묵볶음'],
            '2023-10-25': ['콩나물김칫국', '마파두부덮밥', '후레이크가라아게', '매콤사각어묵볶음', '깍두기/단무지실파무침'],
            '2023-10-26': ['근대된장국', '지코바닭갈비', '비빔막국수', '야채스틱/쌈장', '포기김치/쌈무'],
            '2023-10-27': ['설렁탕/소면', '오징어초무침', '간장떡볶이', '마늘쫑볶음', '섞박지/요구르트']
        }
        data.additional = {
            '2023-10-23': ['돈까스정식'],
            '2023-10-24': ['돈까스정식'],
            '2023-10-26': ['돈까스정식'],
            '2023-10-27': ['돈까스정식']
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
