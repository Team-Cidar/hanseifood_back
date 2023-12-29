from django.db.models import QuerySet
from datetime import datetime
import logging

from typing import Dict, Union, List

from .abstract_service import AbstractService
from ..dtos.daily_menu import DailyMenuDto
from ..repositories.day_repository import DayRepository
from ..repositories.daymeal_repository import DayMealRepository
from ..models import DayMeal, Meal, Day
from .menu_service import MenuService
from ..responses.objs.menu_modification import MenuModificationModel
from ..core.utils.string_utils import parse_str_to_list

logger = logging.getLogger(__name__)


class BackOfficeService(AbstractService):
    def __init__(self):
        # add repository instance variables
        self.__day_repository = DayRepository()
        self.__day_meal_repository = DayMealRepository()
        self.__menu_service = MenuService()

    def add_menus(self, data: Dict[str, Union[str, bool]]) -> MenuModificationModel:
        employee: List[str] = parse_str_to_list(datas=data['employee'])
        student: List[str] = parse_str_to_list(data['student'])
        additional: List[str] = parse_str_to_list(data['additional'])

        date: datetime = datetime.strptime(data['datetime'], "%Y-%m-%d")
        day_entity: QuerySet = self.__day_repository.findByDate(date=date)
        if not day_entity.exists():  # first add
            daily_menu: DailyMenuDto = DailyMenuDto(date=date, student=student, employee=employee,
                                                    additional=additional)
            self.__menu_service.save_daily_menu(data=daily_menu)
            return MenuModificationModel(is_created=True)

        # modify menus
        if len(additional) != 0:
            daymeal_entities: QuerySet = self.__day_meal_repository.findAdditionalByDayId(day_id=day_entity[0])
            self.__put_menus(day_entity=day_entity[0], daymeal_entities=daymeal_entities, menus=additional, for_students=False, is_additional=True)

        if len(student) != 0:
            daymeal_entities: QuerySet = self.__day_meal_repository.findStudentByDayId(day_id=day_entity[0])
            self.__put_menus(day_entity=day_entity[0], daymeal_entities=daymeal_entities, menus=student,
                             for_students=True, is_additional=False)
        if len(employee) != 0:
            daymeal_entities: QuerySet = self.__day_meal_repository.findEmployeeByDayId(day_id=day_entity[0])
            self.__put_menus(day_entity=day_entity[0], daymeal_entities=daymeal_entities, menus=employee, for_students=False, is_additional=False)

        return MenuModificationModel(is_created=False)

    def get_excel_file(self):
        pass

    def __put_menus(self, day_entity: Day, daymeal_entities: QuerySet, menus: list, for_students: bool, is_additional: bool):
        for entity in daymeal_entities:
            self.__day_meal_repository.delete(entity=entity)
        self.__menu_service.save_to_db(day_model=day_entity, datas=menus, for_students=for_students, is_additional=is_additional)