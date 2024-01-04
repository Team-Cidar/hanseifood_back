import os
import dotenv

dotenv.load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
SECRET_KEY = os.getenv('SECRET_KEY')
KAKAO_REST_API_KEY = os.getenv('KAKAO_REST_API_KEY')
KAKAO_API_ADMIN_KEY = os.getenv('KAKAO_API_ADMIN_KEY')
KAKAO_TOKEN_API_URL = os.getenv('KAKAO_TOKEN_API_URL')
KAKAO_REDIRECT_URI = os.getenv('KAKAO_REDIRECT_URI')
KAKAO_USERINFO_API_URL = os.getenv('KAKAO_USERINFO_API_URL')
