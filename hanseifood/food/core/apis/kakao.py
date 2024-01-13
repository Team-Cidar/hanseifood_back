from .request_methods import APIRequests
from ..constants.strings import env_strings as env


class KakaoApi:
    @classmethod
    def request_kakao_token(cls, authorization_code: str) -> str:
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        body: dict = {
            'grant_type': 'authorization_code',
            'client_id': env.KAKAO_REST_API_KEY,
            'redirect_uri': env.KAKAO_REDIRECT_URI,
            'code': authorization_code
        }

        token_response = APIRequests.post(env.KAKAO_TOKEN_API_URL, headers=headers, body=body)
        token_data: dict = token_response.json()
        # refresh_token = token_data['refresh_token']  # kakao refresh token 필요시 사용
        return token_data["access_token"]

    @classmethod
    def request_kakao_user_info(cls, kakao_access_token: str) -> dict:
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Authorization': f'Bearer {kakao_access_token}'
        }

        user_info_response = APIRequests.post(env.KAKAO_USERINFO_API_URL, headers=headers)

        user_data: dict = user_info_response.json()
        user_properties: dict = user_data['properties']
        kakao_id: str = str(user_data['id'])
        kakao_nickname: str = user_properties['nickname']

        return {
            'kakao_id': kakao_id,
            'kakao_nickname': kakao_nickname,
            'kakao_email': ''  # email 동의 항목 추가 이후 함께 return 해야함
        }

