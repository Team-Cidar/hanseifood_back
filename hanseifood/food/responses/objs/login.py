from multipledispatch import dispatch

from .abstract_model import AbstractModel


class UserModel(AbstractModel):
    def __init__(self, kakao_id: str, password: str, email: str, kakao_name: str, is_admin: bool, nickname: str):
        self.kakao_id: str = kakao_id
        self.password: str = password
        self.email: str = email
        self.kakao_name: str = kakao_name
        self.is_admin: bool = is_admin
        self.nickname: str = nickname

    def _serialize(self) -> dict:
        return {
            "kakao_id": self.kakao_id,
            "email": self.email,
            "kakao_name": self.kakao_name,
            "is_admin": self.is_admin,
            "nickname": self.nickname
        }


class UserLoginModel(UserModel):
    def __init__(self,
                 status: bool,
                 kakao_id: str,
                 password: str,
                 email: str,
                 kakao_name: str,
                 is_admin: bool,
                 nickname: str,
                 refresh_token: str = '',
                 access_token: str = ''):
        super(UserLoginModel, self).__init__(kakao_id, password, email, kakao_name, is_admin, nickname)
        self.status: bool = status
        self.refresh_token: str = refresh_token
        self.access_token: str = access_token

    @classmethod
    def from_user_model(cls, status: bool, user_model: UserModel, refresh_token: str = '', access_token: str = ''):
        return cls(
            status=status,
            refresh_token=refresh_token,
            access_token=access_token,
            kakao_id=user_model.kakao_id,
            password=user_model.password,
            email=user_model.email,
            kakao_name=user_model.kakao_name,
            is_admin=user_model.is_admin,
            nickname=user_model.nickname
        )

    def _serialize(self) -> dict:
        return {
            "status": self.status,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "user": super(UserLoginModel, self)._serialize()
        }
