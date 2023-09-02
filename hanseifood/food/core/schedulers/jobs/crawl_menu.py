import os.path
from datetime import datetime
import logging

from ....models import Day, DayMeal, Meal
from ...utils.date_utils import get_dates_in_this_week
from ..modules.crawler import MenuCrawler
from ..modules.excel_parser import ExcelParser

logger = logging.getLogger(__name__)
__all__ = ['get_and_save_menus']  # ~~ import * 로 불러오면 이 함수만 import 됨


# scheduler에 등록할 함수
def get_and_save_menus():
    try:
        logger.info('Execute scheduled job / get_menu_data_schedule')
        # clear all datas
        # Day.objs.all().delete()
        # Meal.objs.all().delete()
        # DayMeal.objs.all().delete()

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
        data, for_both = ExcelParser.parse_excel(path)

        if for_both:
            _save_template1_data(data)  # for both students & employees (during the semester)
        else:
            _save_template2_data(data)  # for only employees (during the vacation)

        logger.info("save finished!")
    except Exception as e:
        logger.error(e)


def _save_template1_data(res):
    for day in res.keys():
        date = datetime.strptime(day, '%Y-%m-%d')

        # check if this day's data exists
        db_day = Day.objects.filter(date=date)
        if db_day.exists():
            logger.info(f'{day} is already exists')
            continue

        db_day = Day(date=date)  # Days
        db_day.save()

        meals_per_day = []
        if type(res[day][0]) is list:  # 메뉴 두개인 날
            std, emp = res[day][0], res[day][1]
            saved_menus = _save_menus(menus=std, is_for_student=True)  # 학생 식당 메뉴 저장
            meals_per_day.extend(saved_menus)  # day_meal table에 data 추가 위한 리스트
            saved_menus = _save_menus(menus=emp, is_for_student=False)  # 교직원 식당 메뉴 저장
            meals_per_day.extend(saved_menus)
        else:  # 메뉴 한개인 날
            saved_menus = _save_menus(menus=res[day], is_for_student=True)
            meals_per_day.extend(saved_menus)

        for menu, for_student in meals_per_day:  # day_meal에 추가
            db_day_meal = DayMeal(day_id=db_day, meal_id=menu, for_student=for_student)
            db_day_meal.save()

        logger.info(f"success to save {day} menu data.")


def _save_template2_data(res):
    for day in res.keys():
        date = datetime.strptime(day, '%Y-%m-%d')

        # check if this day's data exists
        db_day = Day.objects.filter(date=date)
        if db_day.exists():
            logger.info(f'{day} is already exists')
            continue

        db_day = Day(date=date)  # Days
        db_day.save()

        meals_per_day = []
        saved_menus = _save_menus(menus=res[day], is_for_student=False)
        meals_per_day.extend(saved_menus)

        for menu, for_student in meals_per_day:  # day_meal에 추가
            db_day_meal = DayMeal(day_id=db_day, meal_id=menu, for_student=for_student)
            db_day_meal.save()

        logger.info(f"success to save {day} menu data.")


def _save_menus(menus, is_for_student):
    saved_meals = []
    for menu in menus:
        db_meal = Meal.objects.filter(meal_name=menu)  # 음식 저장
        if not db_meal.exists():
            db_meal = Meal(meal_name=menu)  # Meals
            db_meal.save()
        else:
            db_meal = db_meal[0]
        saved_meals.append([db_meal, is_for_student])
    if is_for_student and len(saved_meals) > 5:  # 메뉴 6개 이상이면 마지막껀 교직원용 메뉴임
        saved_meals[-1][1] = False
    return saved_meals
