from typing import List
from django.test import TestCase

from ..dtos.abstract_dto import Dto
from ..enums.role_enums import UserRole


class FriendDto(Dto):
    name: str
    nickname: str
    age: int
    email: str
    role: UserRole


class TestUserDto(Dto):
    name: str
    nickname: str
    age: int
    email: str
    role: UserRole
    friends: List[FriendDto]


class LoginDto(Dto):
    status: bool
    access_token: str
    user: TestUserDto

class MenuResponseDto(Dto):
    def __init__(self, exists: bool, menus: List[str] = None):
        if not exists:
            menus = list()
        self.exists: bool = exists
        self.menus: List[str] = menus
class DailyMenuResponseDto(Dto):
    def __init__(self):
        self.date: str = '20231201'
        self.employee: MenuResponseDto = MenuResponseDto(True, ['a', 'b', 'c', 'd'])
        self.student: MenuResponseDto = MenuResponseDto(True, ['e', 'f', 'g', 'h'])
        self.additional: MenuResponseDto = MenuResponseDto(False)

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
        cls.menu_data = {
            'date': '20231201',
            'employee': {
                'exists': True,
                'menus': ['a', 'b', 'c', 'd']
            },
            'student': {
                'exists': True,
                'menus': ['e', 'f', 'g', 'h']
            },
            'additional': {
                'exists': False,
                'menus': []
            },
        }

    def test_deserializer_serializer(self):
        print('test serializer/deserializer')
        deserialized: LoginDto = LoginDto.deserialize(self.data)
        self.assertEqual(deserialized.serialize(), self.data, 'something wrong')

    def test_response_dto_serialization(self):
        print('test serializer with response dto')
        menus: DailyMenuResponseDto = DailyMenuResponseDto()
        print(menus.serialize())
        self.assertEqual(menus.serialize(), self.menu_data, 'different between serialized data and original data')
