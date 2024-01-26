from .user_dto import UserDto
from ..abstract_dto import Dto
from ...models import MenuLike


class MenuLikeDto(Dto):
    def __init__(self, menu_id: str, user: UserDto):
        self.menu_id: str = menu_id
        self.user_id: UserDto = user

    @classmethod
    def from_model(cls, model: MenuLike):
        menu_like: MenuLikeDto = cls(
            menu_id=str(model.menu_id),
            user=UserDto.from_model(model.user_id)
        )
        return menu_like
