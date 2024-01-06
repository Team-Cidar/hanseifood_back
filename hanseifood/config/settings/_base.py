"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import pymysql
from datetime import timedelta

import food.core.constants.strings.env_strings as env

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.SECRET_KEY

# Application definition
EXCEL_DIR = BASE_DIR / "datas"
if not os.path.exists(EXCEL_DIR):
    os.mkdir(EXCEL_DIR)

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',

    # my apps
    'food',

    # scheduler
    'django_apscheduler',
]

# for scheduler
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

APSCHEDULER_RUN_NOW_TIMEOUT = 25  # default 최대 실행시간

SCHEDULER_DEFAULT = True

############

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'food.middlewares.ip_logging_middleware.IPLoggingMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Check access token in every request. We don't need it. We use decorator to authentication & authorization
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'kakao_id',
    'USER_ID_CLAIM': 'id',

    'TOKEN_OBTAIN_SERIALIZER': "food.core.jwt.serializers.MyTokenObtainPairSerializer",
}

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'food.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False  # True면 models의 datetime에 위 time zone이 반영되지 않음

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WSGI_APPLICATION = 'Kakao.wsgi.application'
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hansei_food',
        'USER': env.DB_USER,
        'PASSWORD': env.DB_PASSWORD,
        'HOST': env.DB_HOST,
        'PORT': env.DB_PORT,
    }
}

# Logger settings
LOG_DIR = BASE_DIR / "logs"
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file_scheduler': {
            'level': 'INFO',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'scheduler.log',
            'formatter': 'standard'
        },
        'file_request': {
            'level': 'INFO',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'server.log',
            'formatter': 'standard'
        },
        'file_error': {
            'level': 'INFO',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'error.log',
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'food.core.schedulers.jobs.crawl_menu': {
            'handlers': ['console', 'file_scheduler'],
            'level': 'DEBUG'
        },
        'food.middlewares': {
            'handlers': ['console', 'file_request'],
            'level': 'INFO',
        },
        'food.utils.menus': {
            'handlers': ['console', 'file_request'],
            'level': 'INFO'
        },
        'food.utils.views': {
            'handlers': ['console', 'file_request'],
            'level': 'INFO'
        },
        'food.responses.error_response': {
            'handlers': ['console', 'file_error'],
            'level': 'INFO'
        }
    }
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = [
    'https://www.hanseiweeklymenu.me',
    'https://hanseiweeklymenu.me',
    'http://www.hanseiweeklymenu.me',
    'http://hanseiweeklymenu.me',
    'http://localhost:8080',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'Authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
CORS_EXPOSE_HEADERS = [
    'Content-Disposition'
]

APPEND_SLASH = False
