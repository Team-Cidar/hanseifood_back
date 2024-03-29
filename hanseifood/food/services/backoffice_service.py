from datetime import datetime, date as Date
import logging

from typing import List, Tuple, Dict
import openpyxl
from django.db.models import QuerySet
from openpyxl.styles import Alignment
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from .abstract_service import AbstractService
from .menu_service import MenuService
from ..core.utils import date_utils, os_utils
from ..core.utils.string_utils import parse_str_to_list
from ..dtos.model_mapped.day_meal_deleted_dto import DayMealDeletedDto
from ..dtos.model_mapped.day_meal_dto import DayMealDto
from ..dtos.requests.add_menu_request_dto import AddMenuRequestDto
from ..dtos.requests.delete_menu_request_dto import DeleteMenuRequestDto
from ..dtos.requests.get_excel_file_request_dto import GetExcelFileRequestDto
from ..dtos.requests.get_menu_history_request_dto import GetMenuHistoryRequestDto
from ..dtos.requests.modify_user_role_request_dto import ModifyUserRoleRequestDto
from ..dtos.responses.common_status_response_dto import CommonStatusResponseDto
from ..dtos.responses.menu_by_id_response_dto import MenuByIdResponseDto
from ..dtos.responses.menu_modification_response_dto import MenuModificationResponseDto
from ..dtos.responses.menu_response_dto import MenuResponseDto
from ..dtos.general.daily_menu import DailyMenuDto
from ..enums.menu_enums import MenuType
from ..enums.role_enums import UserRole
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.jwt_exceptions import PermissionDeniedError
from ..exceptions.request_exceptions import WeekendDateError, PastDateModificationError, InadequateDataError
from ..repositories.daymeal_deleted_repository import DayMealDeletedRepository
from ..repositories.daymeal_repository import DayMealRepository
from ..repositories.day_repository import DayRepository
from ..models import Day, User, DayMeal, DayMealDeleted
from ..repositories.user_respository import UserRepository

logger = logging.getLogger(__name__)


class BackOfficeService(AbstractService):
    def __init__(self):
        self.__day_repository = DayRepository()
        self.__day_meal_repository = DayMealRepository()
        self.__day_meal_deleted_repository = DayMealDeletedRepository()
        self.__user_repository = UserRepository()
        self.__menu_service = MenuService()

    def add_menus(self, data: AddMenuRequestDto) -> MenuModificationResponseDto:
        employee = parse_str_to_list(data.employee)
        student = parse_str_to_list(data.student)
        additional = parse_str_to_list(data.additional)
        date = datetime.strptime(data.datetime, '%Y-%m-%d')

        if date_utils.is_weekend(date):
            raise WeekendDateError(date=date)

        if date_utils.is_past(date):
            raise PastDateModificationError()

        exists, day_queries = self.__day_repository.existByDate(date=date)
        day_model: Day
        if exists:
            day_model = day_queries[0]
            if len(additional) != 0:
                self.__day_meal_repository.deleteByDayIdAndMenuType(day_id=day_model, menu_type=MenuType.ADDITIONAL)
            if len(student) != 0:
                self.__day_meal_repository.deleteByDayIdAndMenuType(day_id=day_model, menu_type=MenuType.STUDENT)
            if len(employee) != 0:
                self.__day_meal_repository.deleteByDayIdAndMenuType(day_id=day_model, menu_type=MenuType.EMPLOYEE)
        else:
            day_model = self.__day_repository.save(date=date)

        daily_menu: DailyMenuDto = DailyMenuDto(date=day_model, student=student, employee=employee, additional=additional)
        self.__menu_service.save_daily_menu(data=daily_menu)

        self.__delete_excel_file(date=date)

        return MenuModificationResponseDto(is_new=not exists)

    def delete_menu(self, data: DeleteMenuRequestDto) -> CommonStatusResponseDto:
        exists, menus = self.__day_meal_repository.existByMenuId(data.menu_id)
        if not exists:
            return CommonStatusResponseDto(True, "menu not exists")

        menu_date: Date = menus[0].day_id.date
        menu_datetime: datetime = datetime(menu_date.year, menu_date.month, menu_date.day)

        if date_utils.is_past(menu_datetime):
            raise PastDateModificationError()

        self.__day_meal_repository.delete_models(menus)

        self.__delete_excel_file(date=menu_datetime)

        return CommonStatusResponseDto()

    def get_menu_history(self, data: GetMenuHistoryRequestDto) -> List[MenuByIdResponseDto]:
        response: List[MenuByIdResponseDto] = []
        exists, days = self.__day_repository.existByDate(datetime.strptime(data.date, '%Y-%m-%d'))
        if not exists:
            raise EmptyDataError(f"{data.date}'s menu is not exists")
        day: Day = days[0]

        menu_dtos: List[DayMealDto] = [DayMealDto.from_model(menu) for menu in self.__day_meal_repository.findByDayIdAndMenuType(day, data.menu_type)]
        if len(menu_dtos) > 0:
            response.append(self.__menu_service.get_menu_by_day_meal_dto(menu_dtos, False))

        menu_history: QuerySet = self.__day_meal_deleted_repository.findByDayIdAndMenuType(day, data.menu_type)
        deleted_menu_dict: Dict[str, List[DayMealDeleted]] = {}

        deleted_menu: DayMealDeleted
        for deleted_menu in menu_history:
            if deleted_menu.menu_id not in deleted_menu_dict.keys():
                deleted_menu_dict[deleted_menu.menu_id] = [deleted_menu]
            else:
                deleted_menu_dict[deleted_menu.menu_id].append(deleted_menu)

        deleted_menus_set = list(deleted_menu_dict.values())
        deleted_menus_set.sort(key=lambda x: x[0].deleted_at, reverse=True)

        for deleted_menus in deleted_menus_set:
            deleted_menu_dtos: List[DayMealDeletedDto] = [DayMealDeletedDto.from_model(item) for item in deleted_menus]
            response.append(self.__menu_service.get_menu_by_day_meal_dto(deleted_menu_dtos, True))

        return response

    def get_excel_file(self, data: GetExcelFileRequestDto):
        date: datetime = datetime.strptime(data.date, "%Y%m%d")

        weekly_menu: MenuResponseDto = self.__menu_service.get_weekly_menu(date=date)
        file_name, exists = self.__check_excel_exists(date=date)
        if not exists:
            template: Workbook = openpyxl.load_workbook("assets/templates/excel_template.xlsx")
            sheet: Worksheet = template.active

            for idx, key in enumerate(weekly_menu.keys):
                col: str = chr(66 + idx)  # starts at B (B ~ F)
                sheet[f"{col}5"] = key
                sheet[f"{col}7"] = ',\n'.join(weekly_menu.employee_menu.get_menus(key))
                sheet[f"{col}12"] = ',\n'.join(weekly_menu.student_menu.get_menus(key))
                sheet[f"{col}17"] = ', '.join(weekly_menu.additional_menu.get_menus(key))

                cell_format: Alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                sheet[f"{col}7"].alignment = cell_format
                sheet[f"{col}12"].alignment = cell_format
                sheet[f"{col}17"].alignment = cell_format

            template.save(f"datas/{file_name}")

            template.close()

        return f"datas/{file_name}"

    def modify_user_role(self, data: ModifyUserRoleRequestDto, requestUser: User) -> CommonStatusResponseDto:
        exists, users = self.__user_repository.existsByKakaoId(kakao_id=data.user_id)
        if not exists:
            raise EmptyDataError(f"There's no such user 'kakao_id={data.user_id}'")

        if requestUser.role == UserRole.MANAGER.value and data.role == UserRole.ADMIN.value:
            raise PermissionDeniedError("Manager can't modify user's role as ADMIN")

        user: User = users[0]
        if user.role == data.role.value:
            return CommonStatusResponseDto(False, msg=f"user already has role of '{data.role}'")

        user.role = data.role.value
        self.__user_repository.update(user)
        return CommonStatusResponseDto(True)

    def __check_excel_exists(self, date: datetime) -> Tuple[str, bool]:
        dates: List[str] = [item.strftime("%Y%m%d") for item in date_utils.get_dates_in_this_week(today=date)]
        file_name: str = f"{dates[0]}-{dates[-1]}.xlsx"
        return file_name, os_utils.check_file_exists(path="datas", file_name=file_name)

    def __delete_excel_file(self, date: datetime):
        file_name, exists = self.__check_excel_exists(date=date)
        if exists:
            os_utils.delete_file(f"datas/{file_name}")
