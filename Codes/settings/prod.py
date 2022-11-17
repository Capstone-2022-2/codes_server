from .base import *
import environ

ALLOWED_HOSTS = ['15.164.3.60']

STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('reviewdb'),
        'USER': env('dbmasteruser'),
        'PASSWORD': env('codes123'),
        'HOST': env('ls-effa51b199b260903146e54b56c8f3687212f536.cudbqywugn2c.ap-northeast-2.rds.amazonaws.com'),
        'PORT': '5432',
    }
}