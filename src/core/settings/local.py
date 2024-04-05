from pathlib import Path

from core.env_reader import env

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = env('BASE_URL')

SECRET_KEY = '123'
DEBUG = True
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = "465"
EMAIL_HOST_USER = "notifications@retmind.com"
EMAIL_HOST_PASSWORD = "witcfaxrkmnzpxhy"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Facebook configuration
FACEBOOK_APP_ID = env('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = env('FACEBOOK_APP_SECRET')

# Google configuration
GOOGLE_CLIENT_ID = env('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = env('GOOGLE_CLIENT_SECRET')

# WeMay app configuration
CLIENT_ID = env('CLIENT_ID')
CLIENT_SECRET = env('CLIENT_SECRET')
