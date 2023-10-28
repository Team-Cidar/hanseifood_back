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
            '2023-10-30',
            '2023-10-31',
            '2023-11-01',
            '2023-11-02',
            '2023-11-03'
        ]
        data.students = {
            '2023-10-30': ['미역국', '돈육바싹불고기', '김말이강정', '콩나물파채무침', '배추김치'],
            '2023-10-31': ['순두부찌개', '함박&파인*소스', '김치메밀전병', '치커리무침', '깍두기'],
            '2023-11-01': ['미니짬뽕국*추가밥', '짜장면', '후르츠만두탕수', '요쿠르트', '단무지', '배추김치'],
            '2023-11-02': ['오징어무국', '돈채청경채볶음', '온두부', '볶음김치', '아채샐러드*드레싱'],
            '2023-11-03': ['유부장국', '햄김치볶음밥', '해물완자전*케찹', '명란젓계란찜', '깍두기/요쿠르트']
        }
        data.employees = {
            '2023-10-30': ['미역국', '돈육바싹불고기', '김말이튀김*강정소스', '콩나물파채무침', '포기김치/양배추찜*쌈장'],
            '2023-10-31': ['순두부찌개', '떡산적스테이크*소스', '김치메밀전병', '연근흑임자무침', '깍두기/치커리무침'],
            '2023-11-01': ['대파육개장', '가자미카레구이', '만두탕수', '두부쑥갓나물', '포기김치/오징어젓무침'],
            '2023-11-02': ['오징어무국', '돈채굴소스청경채볶음', '온두부*볶음김치', '참나물무침', '아채샐러드*드레싱'],
            '2023-11-03': ['유부장국', '햄김치볶음밥', '해물완자전*케찹', '명란젓계란찜/요쿠르트', '총각김치/새우젓호박나물']
        }
        data.additional = {
            '2023-10-30': ['돈까스정식'],
            '2023-10-31': ['돈까스정식'],
            '2023-11-02': ['돈까스정식'],
            '2023-11-03': ['돈까스정식']
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
