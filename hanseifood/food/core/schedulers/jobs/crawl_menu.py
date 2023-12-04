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
<<<<<<< Updated upstream
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
=======
        for date in get_dates_in_this_week(today=datetime.today(), end=6):
            date_str = date.strftime('%Y%m%d')
            if os.path.exists(f'datas/{date_str}.xlsx'):
                logger.info("This week's menu data is already saved")
                return

        # crawling
        crawler = MenuCrawler(driver_path='drivers/chromedriver_local')
        file_name = crawler.crawl()

        logger.info("Crawling job finished!")
>>>>>>> Stashed changes
        logger.info("Start saving datas to database")

        # parse
        # path = 'datas/' + file_name + '.xlsx'

        # data: ParseObject = TempExcelParser.parse(path)  # new template parser
        data: ParseObject = ParseObject()
        data.keys = [
            '2023-11-13',
            '2023-11-14',
            '2023-11-15',
            '2023-11-16',
            '2023-11-17'
        ]
        data.students = {
            '2023-11-13': ['근대된장국', '돈육바베큐폭챱', '쫄면야채무침', '간장어묵볶음', '배추김치'],
            '2023-11-14': ['사골물만둣국', '부추산적구이', '두부조림', '모닝빵샌드위치', '깍두기'],
            '2023-11-15': ['미니우동(면)', '김치밥버거', '고구마고초케/케찹', '콩나물무침', '깍두기'],
            '2023-11-16': ['계란부추국', '마파두부덮밥', '치킨까스*머스타드', '만두강정', '배추김치'],
            '2023-11-17': ['열무된장국', '순살당면찜닭', '매콤누들떡볶이', '청경채겉절이', '배추김치']
        }
        data.employees = {
            '2023-11-13': ['근대된장국', '돈육바베큐폭챱', '쫄면야채무침', '간장어묵볶음', '포기김치/오이부추무침'],
            '2023-11-14': ['사골물만둣국', '부추산적구이', '두부조림', '참나물유자청무침', '깍두기/모닝빵샌드위치'],
            '2023-11-15': ['어묵우동국', '소고기콩나물밥*양념장', '코다리강정', '새송이감자조림', '깍두기/가지나물'],
            '2023-11-16': ['계란부추국', '마파두부덮밥', '치킨까스*머스타드', '만두강정', '포기김치/그린샐러드'],
            '2023-11-17': ['열무된장국', '순살당면찜닭', '매콤누들떡볶이', '쑥갓두부무침', '포기김치/청경채겉절이']
        }
        data.additional = {
            '2023-11-13': ['돈까스정식'],
            '2023-11-14': ['돈까스정식'],
            '2023-11-16': ['설렁탕*소면', '김치메밀전병', '깍두기', '요쿠르트'],
            '2023-11-17': ['돈까스정식']
        }
        _save_data_temp(data)

        logger.info("save finished!")
    except Exception as e:
        logger.error(e)
        data: ParseObject = ParseObject()
        data.keys = [
            '2023-11-13',
            '2023-11-14',
            '2023-11-15',
            '2023-11-16',
            '2023-11-17'
        ]
        data.students = {
            '2023-11-13': ['근대된장국', '돈육바베큐폭챱', '쫄면야채무침', '간장어묵볶음', '배추김치'],
            '2023-11-14': ['사골물만둣국', '부추산적구이', '두부조림', '모닝빵샌드위치', '깍두기'],
            '2023-11-15': ['미니우동(면)', '김치밥버거', '고구마고초케/케찹', '콩나물무침', '깍두기'],
            '2023-11-16': ['계란부추국', '마파두부덮밥', '치킨까스*머스타드', '만두강정', '배추김치'],
            '2023-11-17': ['열무된장국', '순살당면찜닭', '매콤누들떡볶이', '청경채겉절이', '배추김치']
        }
        data.employees = {
            '2023-11-13': ['근대된장국', '돈육바베큐폭챱', '쫄면야채무침', '간장어묵볶음', '포기김치/오이부추무침'],
            '2023-11-14': ['사골물만둣국', '부추산적구이', '두부조림', '참나물유자청무침', '깍두기/모닝빵샌드위치'],
            '2023-11-15': ['어묵우동국', '소고기콩나물밥*양념장', '코다리강정', '새송이감자조림', '깍두기/가지나물'],
            '2023-11-16': ['계란부추국', '마파두부덮밥', '치킨까스*머스타드', '만두강정', '포기김치/그린샐러드'],
            '2023-11-17': ['열무된장국', '순살당면찜닭', '매콤누들떡볶이', '쑥갓두부무침', '포기김치/청경채겉절이']
        }
        data.additional = {
            '2023-11-13': ['돈까스정식'],
            '2023-11-14': ['돈까스정식'],
            '2023-11-16': ['설렁탕*소면', '김치메밀전병', '깍두기', '요쿠르트'],
            '2023-11-17': ['돈까스정식']
        }
        _save_data_temp(data)


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
