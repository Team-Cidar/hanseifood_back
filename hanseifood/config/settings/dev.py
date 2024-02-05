from ._base import *
import socket

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]
WSGI_APPLICATION = 'config.wsgi.dev.application'
print('Development mode!')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
CORS_ALLOWED_ORIGINS.append(f"http://{s.getsockname()[0]}:8080")  # bind host of localhost
s.close()
print(CORS_ALLOWED_ORIGINS[-1])