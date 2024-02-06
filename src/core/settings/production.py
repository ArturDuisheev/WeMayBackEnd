from core.env_reader import env, csv

# SECRET_KEY
SECRET_KEY = env('SECRET_KEY')

# DEBUG
DEBUG = env('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS
ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=csv())

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT', cast=int),
    }
}


