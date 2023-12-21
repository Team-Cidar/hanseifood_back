from datetime import datetime
import logging

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
        # logger.info('Execute scheduled job / get_menu_data_schedule')
        # clear all datas
        # day_repository.clearAll()
        # meal_repository.clearAll()
        # day_meal_repository.clearAll()

        # check if already did crawling
        # for date in get_dates_in_this_week(today=datetime.today(), end=6):
        #     date_str = date.strftime('%Y%m%d')
        #     if os.path.exists(f'datas/{date_str}.xlsx'):
        #         logger.info("This week's menu data is already saved")
        #         return
        #
        # # crawling
        # crawler = MenuCrawler(driver_path=os.getenv("CHROME_DRIVER_PATH"))
        # file_name = crawler.crawl()
        #
        # logger.info("Crawling job finished!")
        logger.info("Start saving datas to database")

        # parse
        # path = 'datas/' + file_name + '.xlsx'

        # data: ParseObject = TempExcelParser.parse(path)  # new template parser
        data: ParseObject = ParseObject()
        data.keys = [
            '2023-12-18',
            '2023-12-19',
            '2023-12-20',
            '2023-12-21',
            '2023-12-22'
        ]
        data.students = {
            '2023-12-18': ['참치김치찌개', '함박스테이크', '토마토펜네파스타', '그린샐러드/키위드레싱', '깍두기'],
            '2023-12-19': ['감자수제비국', '돈사태김치찜', '봉어묵조림', '고구마고로케*케찹', '깍두기'],
            '2023-12-20': ['추가백미밥', '꼬치어묵우동(면)', '신전떡볶이', '찐순대*소금', '김말이튀김,단무지'],
            '2023-12-21': ['시금치된장국', '안동찜닭', '김치녹두전*양념장', '미니밤만쥬', '배추김치'],
        }
        data.employees = {
            '2023-12-18': ['참치김치찌개', '함박스테이크*소스', '토마토펜네파스타', '감자채볶음', '섞박지/돌나물샐러드'],
            '2023-12-19': ['감자수제비국', '돈사태김치찜', '봉어묵조림', '미역레몬무침', '깍두기/무들깨나물'],
            '2023-12-20': ['감자옹심이만두국', '소고기콩나물밥*양념장', '고등어무조림', '김말이튀김*강정소스', '포기김치/과일샐러드'],
            '2023-12-21': ['시금치된장국', '안동찜닭', '김치녹두전*양념장', '얼갈이무침', '포기김치/사과주스'],
            '2023-12-22': ['나가사끼짬뽕국', '해물동그랑땡전*케찹', '두부조림', '단무지쪽파무침', '포기김치/미니찐빵']
        }
        data.additional = {
            '2023-12-18': ['돈까스정식'],
            '2023-12-19': ['돈까스정식'],
            '2023-12-21': ['돈까스정식'],
            '2023-12-22': ['돈까스정식']
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
            # 메뉴가 존재하지 않는 날은 dict key에러가 나서 그냥 넘어가도록 처리, student, employee, additinal 모두 해당
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
