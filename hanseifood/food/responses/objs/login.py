from .abstract_model import AbstractModel


class UserModel(AbstractModel):
    def __init__(self, user_id: str, user_nickname: str, is_exists: bool, customnickname: str, access_token: str):
        self.user_id = user_id
        self.user_nickname = user_nickname
        self.is_exists = is_exists
        self.customnickname = customnickname
        self.access_token = access_token

    def _serialize(self) -> dict:
        return {
            "id": self.user_id,
            "kakaonickname": self.user_nickname,
            "isExists": str(self.is_exists).lower(),  # Convert bool to string
            "customnickname": self.customnickname,
            "access_token": self.access_token
        }
