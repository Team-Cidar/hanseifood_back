from ..abstract_dto import Dto


class AddCommentRequestDto(Dto):
    menu_id: str
    comment: str