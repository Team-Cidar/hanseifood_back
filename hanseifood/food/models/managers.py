from django.contrib.auth.models import BaseUserManager

from ..core.enums.role_enums import UserRole
from ..exceptions.data_exceptions import DBFieldError


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, nickname: str, kakao_name: str, kakao_id: str, role: UserRole):
        if not kakao_id:
            raise DBFieldError("Kakao Id field is required but not given.")

        user = self.model(email=self.normalize_email(email), nickname=nickname, kakao_name=kakao_name, kakao_id=kakao_id)
        user.set_password(kakao_id)
        user.role = str(role)
        user.save()
        return user

    def create_superuser(self, email: str, nickname: str, kakao_name: str, kakao_id: str):
        user = self.create_user(
            email=email,
            nickname=nickname,
            kakao_name=kakao_name,
            kakao_id=kakao_id,
            role=UserRole.A
        )
        user.is_admin = True
        user.save()
        return user
