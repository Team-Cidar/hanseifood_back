import os.path
from datetime import datetime
import logging

from ...utils.date_utils import get_dates_in_this_week
from ..modules.crawler import MenuCrawler
from ..modules.excel_parser import ExcelParser
from ..modules.temp_excel_parser import TempExcelParser
from ....repositories.day_repository import DayRepository
from ....repositories.daymeal_repository import DayMealRepository
from ....repositories.meal_repository import MealRepository

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

        data = TempExcelParser.parse(path)  # new template temp parser
        _save_data_temp(data)

        # data, for_both = ExcelParser.parse_excel(path)
        #
        # if for_both:
        #     _save_template1_data(data)  # for both students & employees (during the semester)
        # else:
        #     _save_template2_data(data)  # for only employees (during the vacation)

        logger.info("save finished!")
    except Exception as e:
        logger.error(e)


def _save_data_temp(data):
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


# def _save_template1_data(res):
#     for day in res.keys():
#         date = datetime.strptime(day, '%Y-%m-%d')
#
#         # check if this day's data exists
#         db_day = day_repository.findByDate(date)
#         if db_day.exists():
#             logger.info(f'{day} is already exists')
#             continue
#
#         db_day = day_repository.save(date)
#
#         meals_per_day = []
#         if type(res[day][0]) is list:  # 메뉴 두개인 날
#             std, emp = res[day][0], res[day][1]
#             saved_menus = _save_menus(menus=std, is_for_student=True)  # 학생 식당 메뉴 저장
#             meals_per_day.extend(saved_menus)  # day_meal table에 data 추가 위한 리스트
#             saved_menus = _save_menus(menus=emp, is_for_student=False)  # 교직원 식당 메뉴 저장
#             meals_per_day.extend(saved_menus)
#         else:  # 메뉴 한개인 날
#             saved_menus = _save_menus(menus=res[day], is_for_student=True)
#             meals_per_day.extend(saved_menus)
#
#         for menu, for_student in meals_per_day:  # day_meal에 추가
#             day_meal_repository.save(db_day, menu, for_student)
#
#         logger.info(f"success to save {day} menu data.")
#
#
# def _save_template2_data(res):
#     for day in res.keys():
#         date = datetime.strptime(day, '%Y-%m-%d')
#
#         # check if this day's data exists
#         db_day = day_repository.findByDate(date)
#
#         if db_day.exists():
#             logger.info(f'{day} is already exists')
#             continue
#
#         db_day = day_repository.save(date)
#
#         meals_per_day = []
#         saved_menus = _save_menus(menus=res[day], is_for_student=False)
#         meals_per_day.extend(saved_menus)
#
#         for menu, for_student in meals_per_day:  # day_meal에 추가
#             day_meal_repository.save(db_day, menu, for_student)
#
#         logger.info(f"success to save {day} menu data.")
#
#
# def _save_menus(menus, is_for_student):
#     saved_meals = []
#     for menu in menus:
#         db_meal = meal_repository.findByMenuName(menu)
#         if not db_meal.exists():
#             db_meal = meal_repository.save(meal_name=menu)
#         else:
#             db_meal = db_meal[0]
#         saved_meals.append([db_meal, is_for_student])
#     if is_for_student and len(saved_meals) > 5:  # 메뉴 6개 이상이면 마지막껀 교직원용 메뉴임
#         saved_meals[-1][1] = False
#     return saved_meals
