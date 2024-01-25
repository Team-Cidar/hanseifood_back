import logging
from typing import List

from django.db.models import QuerySet

from .abstract_service import AbstractService
from ..dtos.model_mapped.comment_deleted_dto import CommentDeletedDto
from ..dtos.model_mapped.comment_report_dto import CommentReportDto
from ..dtos.model_mapped.menu_comment_dto import MenuCommentDto
from ..dtos.requests.add_comment_request_dto import AddCommentRequestDto
from ..dtos.requests.delete_comment_request_dto import DeleteCommentRequestDto
from ..dtos.requests.get_comment_request_dto import GetCommentRequestDto
from ..dtos.requests.report_comment_request_dto import ReportCommentRequestDto
from ..dtos.responses.comment_response_dto import CommentResponseDto, DeletedCommentResponseDto
from ..dtos.responses.common_status_response_dto import CommonStatusResponseDto
from ..dtos.responses.reported_comment_response_dto import ReportedCommentResponseDto
from ..enums.report_type_enums import ReportType
from ..enums.role_enums import UserRole
from ..exceptions.data_exceptions import EmptyDataError
from ..exceptions.jwt_exceptions import PermissionDeniedError
from ..exceptions.request_exceptions import EmptyValueError
from ..models import User, MenuComment, CommentDeleted
from ..repositories.comment_deleted_repository import CommentDeletedRepository
from ..repositories.comment_report_repository import CommentReportRepository
from ..repositories.daymeal_repository import DayMealRepository
from ..repositories.menu_comment_repository import MenuCommentRepository

logger = logging.getLogger(__name__)


class CommentService(AbstractService):
    def __init__(self):
        self.__day_meal_repository = DayMealRepository()
        self.__menu_comment_repository = MenuCommentRepository()
        self.__comment_report_repository = CommentReportRepository()
        self.__comment_deleted_repository = CommentDeletedRepository()

    def add_comment(self, data: AddCommentRequestDto, user: User) -> CommentResponseDto:
        exists, menus = self.__day_meal_repository.existByMenuId(menu_id=data.menu_id)
        if not exists:
            raise EmptyDataError(f"Menus with id '{data.menu_id}' are not exists")

        menu_comment_model: MenuComment = self.__menu_comment_repository.save(
            menu_id=data.menu_id,
            comment=data.comment,
            user_id=user
        )
        return CommentResponseDto(MenuCommentDto.from_model(menu_comment_model))

    def delete_comment(self, data: DeleteCommentRequestDto, user: User):
        exists, comments = self.__menu_comment_repository.existByCommentId(comment_id=data.comment_id)
        if not exists:
            raise EmptyDataError(f"Comment with id '{data.comment_id}' is not exists")

        comment: MenuComment = comments[0]
        if user.role == UserRole.ADMIN:
            self.__menu_comment_repository.delete(comment)
            return CommonStatusResponseDto(True)

        if comment.user_id != user:
            raise PermissionDeniedError("Trying to delete other user's comment")

        self.__menu_comment_repository.delete(comment)
        return CommonStatusResponseDto(True)

    def get_comment_by_menu_id(self, data: GetCommentRequestDto) -> List[CommentResponseDto]:
        exists, menus = self.__day_meal_repository.existByMenuId(menu_id=data.menu_id)
        if not exists:
            raise EmptyDataError(f"Menus with id '{data.menu_id}' are not exists")

        response: List[CommentResponseDto] = []
        exists, comments = self.__menu_comment_repository.existByMenuId(menu_id=data.menu_id)
        if not exists:
            return response

        for comment in comments:
            response.append(CommentResponseDto(MenuCommentDto.from_model(comment)))

        return response

    def get_comment_by_user(self, user: User) -> List[CommentResponseDto]:
        comment_models: QuerySet = self.__menu_comment_repository.findByUserId(user_id=user)
        response: List[CommentResponseDto] = []
        for model in comment_models:
            response.append(CommentResponseDto(MenuCommentDto.from_model(model)))

        return response

    def report_comment(self, data: ReportCommentRequestDto, user: User) -> CommonStatusResponseDto:
        exists, comments = self.__menu_comment_repository.existByCommentId(data.comment_id)
        if not exists:
            raise EmptyDataError(f"Comment with id '{data.comment_id}' is deleted or not exists.")

        if data.report_type is ReportType.ETC and len(data.report_msg) == 0:
            raise EmptyValueError(msg=f'reportMsg field is required with ReportType.ETC. But not given.')

        self.__comment_report_repository.save(
            comment_id=data.comment_id,
            reporter=user,
            report_type=data.report_type,
            report_msg=data.report_msg
        )

        return CommonStatusResponseDto(True)

    def get_reported_comments(self) -> List[ReportedCommentResponseDto]:
        reported_comments: List[CommentReportDto] = [CommentReportDto.from_model(model) for model in self.__comment_report_repository.all()]
        response: List[ReportedCommentResponseDto] = []
        for r_comment in reported_comments:
            exists, comment_models = self.__menu_comment_repository.existByCommentId(comment_id=r_comment.comment_id)
            if not exists:
                # find in deleted
                deleted_comments: QuerySet = self.__comment_deleted_repository.findByCommentId(comment_id=r_comment.comment_id)
                deleted_comment_model: CommentDeleted = deleted_comments[0]
                deleted_comment_dto: CommentDeletedDto = CommentDeletedDto.from_model(deleted_comment_model)
                deleted_comment_response: DeletedCommentResponseDto = DeletedCommentResponseDto(deleted_comment_dto)
                response.append(ReportedCommentResponseDto(r_comment, deleted_comment_response))
                continue
            comment_model: MenuComment = comment_models[0]
            comment_dto: MenuCommentDto = MenuCommentDto.from_model(comment_model)
            comment_response: CommentResponseDto = CommentResponseDto(comment_dto)
            response.append(ReportedCommentResponseDto(r_comment, comment_response))
        return response