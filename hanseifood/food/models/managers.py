from django.contrib.auth.models import BaseUserManager

from ..exceptions.data_exceptions import DBFieldError


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, nickname: str, kakao_name: str):
        if not email:
            raise DBFieldError("Email field is required but not given.")

        user = self.model(email=self.normalize_email(email), nickname=nickname, kakao_name=kakao_name)
        user.set_password(self.make_random_password())
        user.save()
        return user

    def create_superuser(self, email: str, nickname: str, kakao_name: str):
        user = self.create_user(
            email=email,
            nickname=nickname,
            kakao_name=kakao_name
        )
        user.is_admin = True
        user.save()
        return user
