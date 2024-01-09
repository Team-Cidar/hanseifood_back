from django.db.models import QuerySet
from typing import Tuple
from datetime import datetime

from .abstract_repository import AbstractRepository
from ..enums.role_enums import UserRole
from ..models import User


class UserRepository(AbstractRepository):
    def __init__(self):
        super(UserRepository, self).__init__(User.objects)

    def findByKakaoId(self, kakao_id: str) -> QuerySet:
        datas: QuerySet = self.manager.filter(kakao_id=kakao_id)
        return datas

    def existsByKakaoId(self, kakao_id: str) -> Tuple[bool, QuerySet]:
        datas: QuerySet = self.findByKakaoId(kakao_id=kakao_id)
        return datas.exists(), datas

    def modifyLastLoginByUser(self, user: User) -> User:
        user.last_login = datetime.today()
        user.save(update_fields=['last_login'])  # prevent updating update_at field also
        return user

    # override
    def save(self, email: str, nickname: str, kakao_name: str, kakao_id: str, role: UserRole) -> User:
        entity: User = self.manager.create_user(
            email=email,
            nickname=nickname,
            kakao_name=kakao_name,
            kakao_id=kakao_id,
            role=role)
        return entity
