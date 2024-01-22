import logging
from typing import List

from django.db.models import QuerySet

from .abstract_service import AbstractService
from ..dtos.model_mapped.menu_comment_dto import MenuCommentDto
from ..dtos.requests.add_comment_request_dto import AddCommentRequestDto
from ..dtos.requests.get_comment_request_dto import GetCommentRequestDto
from ..dtos.responses.comment_response_dto import CommentResponseDto
from ..exceptions.data_exceptions import EmptyDataError
from ..models import User, MenuComment
from ..repositories.daymeal_repository import DayMealRepository
from ..repositories.menu_comment_repository import MenuCommentRepository

logger = logging.getLogger(__name__)


class CommentService(AbstractService):
    def __init__(self):
        self.__day_meal_repository = DayMealRepository()
        self.__menu_comment_repository = MenuCommentRepository()

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

