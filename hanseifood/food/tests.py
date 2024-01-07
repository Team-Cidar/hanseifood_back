from typing import List

from django.test import TestCase

from .dtos.abstract_dto import Dto
from .enums.role_enums import UserRole


class FriendDto(Dto):
    name: str
    nickname: str
    age: int
    email: str
    role: UserRole


class UserDto(Dto):
    name: str
    nickname: str
    age: int
    email: str
    role: UserRole
    friends: List[FriendDto]


class LoginDto(Dto):
    status: bool
    access_token: str
    user: UserDto

class DtoTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'status': True,
            'access_token': "user access token is here",
            'user': {
                'name': 'Jeremy',
                'nickname': 'django',
                'age': 25,
                'email': 'tmd24710@naver.com',
                'role': 'A',
                'friends': [
                    {
                        'name': 'Jeremy',
                        'nickname': 'django',
                        'age': 25,
                        'email': 'psw24710@gmail.com',
                        'role': 'U'
                    },
                    {
                        'name': 'Park',
                        'nickname': 'python',
                        'age': 24,
                        'email': 'tmd24710@gmail.com',
                        'role': 'U'
                    },
                ]
            },
        }

    def test_deserializer_serializer(self):
        deserialized: LoginDto = LoginDto.deserialize(self.data)
        self.assertEqual(deserialized.serialize(), self.data, 'something wrong')