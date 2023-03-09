"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '.localhost',
    # '127.0.0.1',
    # '[::1]',
    'gaialabs.ai',
    'ip.gaialabs.ai',
    'home.gaialabs.ai',
    # 'chrome-extension://ghkjadifhfhebgfbcmgoklkkhapjjmbj'
]


# Application definition
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'knox.auth.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'new_app',
    'rest_framework',
    'knox',
    'corsheaders',
    'django_crontab'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'new_app.my_csrf_middleware.MyCsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'main_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates'), os.path.join(PROJECT_ROOT, 'static')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'main_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'main': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'my-sql': { # : MySQL 5.7 or later is required (found 5.6.51)
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  os.environ['MYSQL_DB'],
        'USER':  os.environ['MYSQL_USER'],
        'PASSWORD': os.environ['MYSQL_PASSWORD'],
        'HOST': os.environ['MYSQL_HOST'],   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
default_database = os.environ.get('DJANGO_DATABASE', 'main')
DATABASES['default'] = DATABASES[default_database]


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

MEDIA_ROOT = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ALLOWED_HOSTS=['*']
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://gaialabs.ai',
    'http://ip.gaialabs.ai',
    'http://home.gaialabs.ai',
    'https://ec2-13-230-184-34.ap-northeast-1.compute.amazonaws.com',
    # 'chrome-extension://ghkjadifhfhebgfbcmgoklkkhapjjmbj'
]
CORS_ALLOWED_ORIGIN = [
    'chrome-extension://ghkjadifhfhebgfbcmgoklkkhapjjmbj',
    'chrome-extension://gagdcpbjnijopmfdodmienpomniggmbn'
    'http://gaialabs.ai',
    'http://ip.gaialabs.ai',
    'http://home.gaialabs.ai',
    # 'http://localhost:4200',
    # 'http://localhost:4201'
]
CSRF_TRUSTED_ORIGINS = [
    'http://gaialabs.ai',
    'http://ip.gaialabs.ai',
    'http://home.gaialabs.ai',
    'chrome-extension://ghkjadifhfhebgfbcmgoklkkhapjjmbj',
    'chrome-extension://gagdcpbjnijopmfdodmienpomniggmbn'
]
# must have this CSRF_HEADER_NAME 'CSRF_COOKIE' when using chrome extension
CSRF_HEADER_NAME = 'CSRF_COOKIE'
# CSRF_COOKIE_PATH = '/'
# CSRF_COOKIE_SAMESITE = 'Strict'
# CSRF_COOKIE_SECURE = True

# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_SAMESITE = None
# CSRF_COOKIE_SAMESITE = 'None'
# CSRF_COOKIE_HTTPONLY = False
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "gaia-ai-token",
]

CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL="new_app.User"

PASSWORD_RESET_EXPIRATION_TIME = 1 * 60 * 10 # 10 minutes

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# CRONJOBS = [
#     ('* * * * *', 'new_app.cron_jobs.send_emails.start')
# ]
