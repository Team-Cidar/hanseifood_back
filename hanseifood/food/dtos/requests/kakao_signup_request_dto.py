from ..abstract_dto import Dto


class KakaoSignupRequestDto(Dto):
    kakao_id: str
    email: str
    kakao_name: str
    nickname: str