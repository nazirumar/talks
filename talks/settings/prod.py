from .base import *
from decouple import config

DEBUG = False
ADMINS = [
    ("admin", "admin@gmail.com"),
]
ALLOWED_HOSTS = ['.talksproject.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True