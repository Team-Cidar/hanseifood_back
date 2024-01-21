import logging


from .abstract_service import AbstractService
from ..dtos.model_mapped.menu_comment_dto import MenuCommentDto
from ..dtos.model_mapped.user_dto import UserDto
from ..dtos.requests.add_comment_request_dto import AddCommentRequestDto
from ..exceptions.data_exceptions import EmptyDataError
from ..models import User, MenuComment
from ..repositories.daymeal_repository import DayMealRepository
from ..repositories.menu_comment_repository import MenuCommentRepository

logger = logging.getLogger(__name__)


class CommentService(AbstractService):
    def __init__(self):
        self.__day_meal_repository = DayMealRepository()
        self.__menu_comment_repository = MenuCommentRepository()

    def add_comment(self, data: AddCommentRequestDto, user: User) -> MenuCommentDto:
        exists, menus = self.__day_meal_repository.existByMenuId(menu_id=data.menu_id)
        if not exists:
            raise EmptyDataError(f"Menus with id '{data.menu_id}' are not exists")

        menu_comment_model: MenuComment = self.__menu_comment_repository.save(
            menu_id=data.menu_id,
            comment=data.comment,
            user_id=user
        )
        return MenuCommentDto.from_model(menu_comment_model)