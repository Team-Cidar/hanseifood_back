from ..abstract_dto import Dto
from ...enums.role_enums import UserRole


class ModifyUserRoleRequestDto(Dto):
    user_id: str
    role: UserRole