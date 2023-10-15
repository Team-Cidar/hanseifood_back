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
            '2023-10-16',
            '2023-10-17',
            '2023-10-18',
            '2023-10-19',
            '2023-10-20'
        ]
        data.students = {
            '2023-10-16': ['감자된장국', '카레라이스', '춘권튀김', '들기름막국수', '배추김치'],
            '2023-10-17': ['맑은콩나물국', '묵은지닭볶음탕', '어니언튀김/케찹', '들깨미역줄기볶음', '깍두기'],
            '2023-10-18': ['유부된장국', '추가백미밥', '김말이강정', '요쿠르트', '단무지', '배추김치'],
            '2023-10-19': ['얼큰순댓국', '생선가스/타르s', '소세지야채볶음', '도시락김', '깍두기'],
            '2023-10-20': ['짬뽕순두부찌개', '탕수육/소스', '버섯감자조림', '콩나물무침', '배추김치']
        }
        data.employees = {
            '2023-10-16': ['감자된장국', '소세지카레라이스', '춘권튀김', '들기름막국수', '포기김치/요쿠르트'],
            '2023-10-17': ['맑은콩나물국', '묵은지닭볶음탕', '어니언튀김/케찹', '마늘쫑무침', '갓김치/들깨미역줄기'],
            '2023-10-18': ['유부된장국', '포크퀘사디아', '또띠아/샤워크림', '그린샐러드', '포기김치/콩나물무침'],
            '2023-10-19': ['얼큰순댓국', '생선가스/타르s', '청경채볶음우동', '호박나물', '섞박지/도시락김'],
            '2023-10-20': ['짬뽕순두부찌개', '탕수육/소스', '버섯감자조림', '가지튀김', '포기김치']
        }
        data.additional = {
            '2023-10-16': ['돈까스정식'],
            '2023-10-17': ['돈까스정식'],
            '2023-10-19': ['돈까스정식'],
            '2023-10-20': ['돈까스정식']
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
