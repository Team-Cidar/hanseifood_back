import uuid
from datetime import datetime
import logging

from typing import List, Union

from .abstract_service import AbstractService
from ..core.utils import date_utils
from ..dtos.model_mapped.day_meal_deleted_dto import DayMealDeletedDto
from ..dtos.model_mapped.day_meal_dto import DayMealDto
from ..dtos.general.daily_menu import DailyMenuDto
from ..dtos.responses.menu_by_id_response_dto import DeletedMenuByIdResponseDto, MenuByIdResponseDto
from ..dtos.responses.menu_response_dto import MenuResponseDto
from ..enums.menu_enums import MenuType
from ..exceptions.data_exceptions import EmptyDataError
from ..repositories.day_repository import DayRepository
from ..repositories.daymeal_deleted_repository import DayMealDeletedRepository
from ..repositories.daymeal_repository import DayMealRepository
from ..repositories.meal_repository import MealRepository
from ..models import Day
from ..repositories.menu_comment_repository import MenuCommentRepository
from ..repositories.menu_like_repository import MenuLikeRepository

logger = logging.getLogger(__name__)


class MenuService(AbstractService):
    def __init__(self):
        self.__day_repository = DayRepository()
        self.__day_meal_repository = DayMealRepository()
        self.__day_meal_deleted_repository = DayMealDeletedRepository()
        self.__meal_repository = MealRepository()
        self.__menu_like_repository = MenuLikeRepository()
        self.__menu_comment_repository = MenuCommentRepository()

    def get_today_menu(self) -> MenuResponseDto:
        return self.get_target_days_menu(datetime.today())

    def get_weekly_menu(self, date: datetime = datetime.today()) -> MenuResponseDto:
        this_week: List[datetime] = date_utils.get_dates_in_this_week(today=date)

        response: MenuResponseDto = MenuResponseDto()

        date: datetime
        for date in this_week:
            response += self.__get_daily_menus(date=date)

        return response

    def get_target_days_menu(self, date: datetime) -> MenuResponseDto:
        date = date_utils.get_weekday(date)  # to get friday when today is 'sat' or 'sun'
        return self.__get_daily_menus(date=date)

    def save_daily_menu(self, data: DailyMenuDto) -> None:
        self.__save_daily_menus_to_db(day_model=data.date, datas=data.student, menu_type=MenuType.STUDENT)
        self.__save_daily_menus_to_db(day_model=data.date, datas=data.employee, menu_type=MenuType.EMPLOYEE)
        self.__save_daily_menus_to_db(day_model=data.date, datas=data.additional, menu_type=MenuType.ADDITIONAL)

    def get_by_menu_id(self, menu_id: str) -> MenuByIdResponseDto:
        menu_dto: MenuByIdResponseDto
        like_count: int = self.__menu_like_repository.countByMenuId(menu_id)
        comment_count: int = self.__menu_comment_repository.countByMenuId(menu_id)
        exists, menus = self.__day_meal_repository.existByMenuId(menu_id=menu_id)
        if not exists:
            exists, deleted_menus = self.__day_meal_deleted_repository.existByMenuId(menu_id=menu_id)
            if not exists:
                raise EmptyDataError(f"Menu with id '{menu_id}' is not exists")
            menu_dto = DeletedMenuByIdResponseDto(
                deleted_menu_dtos=[DayMealDeletedDto.from_model(deleted_menu) for deleted_menu in deleted_menus],
                like_count=like_count,
                comment_count=comment_count
            )
        else:
            menu_dto = MenuByIdResponseDto(
                day_meal_dtos=[DayMealDto.from_model(menu) for menu in menus],
                like_count=like_count,
                comment_count=comment_count
            )
        return menu_dto

    def get_menu_by_day_meal_dto(self, dtos, deleted: bool):
        menu_id: str = dtos[0].menu_id
        like_count: int = self.__menu_like_repository.countByMenuId(menu_id)
        comment_count: int = self.__menu_comment_repository.countByMenuId(menu_id)
        if deleted:
            return DeletedMenuByIdResponseDto(
                deleted_menu_dtos=dtos,
                like_count=like_count,
                comment_count=comment_count
            )
        return MenuByIdResponseDto(
            day_meal_dtos=dtos,
            like_count=like_count,
            comment_count=comment_count
        )

    def __get_daily_menus(self, date: datetime) -> MenuResponseDto:
        weekday_kor: str = date_utils.get_weekday_kor(date)
        key: str = f'{date.strftime("%Y-%m-%d")} ({weekday_kor})'

        result: MenuResponseDto = MenuResponseDto(key)

        exists, day_queries = self.__day_repository.existByDate(date=date)
        if not exists:
            return result

        day_model: Day = day_queries[0]

        for menu_type in MenuType.get_all_except_default():
            exists, menu_queries = self.__day_meal_repository.existByDayIdAndMenuType(day_id=day_model, menu_type=menu_type)
            if not exists:
                continue
            day_meal_dtos: List[DayMealDto] = [DayMealDto.from_model(item) for item in menu_queries]
            menu_id: str = day_meal_dtos[0].menu_id
            like_count: int = self.__menu_like_repository.countByMenuId(menu_id=menu_id)
            comment_count: int = self.__menu_comment_repository.countByMenuId(menu_id=menu_id)
            result.add_menus_by_type(
                _type=menu_type,
                date_key=key,
                day_meal_dtos=day_meal_dtos,
                like_count=like_count,
                comment_count=comment_count
            )

        return result

    def __save_daily_menus_to_db(self, day_model, datas: list, menu_type: MenuType):
        daily_menu_id: str = str(uuid.uuid4())
        for menu in datas:
            menu_model = self.__meal_repository.findByMenuName(menu)
            if not menu_model.exists():
                menu_model = self.__meal_repository.save(menu)
            else:
                menu_model = menu_model[0]

            self.__day_meal_repository.save(day_id=day_model, meal_id=menu_model, menu_type=menu_type, menu_id=daily_menu_id)
