from ._base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['localhost', 'hanseiweeklymenu.me', 'www.hanseiweeklymenu.me', '218.239.156.31']
WSGI_APPLICATION = 'config.wsgi.prod.application'
print("Production mode!")
