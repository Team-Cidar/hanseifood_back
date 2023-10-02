from ._base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]
WSGI_APPLICATION = 'config.wsgi.dev.application'
print('Development mode!')