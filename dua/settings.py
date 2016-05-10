"""
Django settings for dua project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import mongoengine

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c=s#fabs%s+iksjnsg*p=0=k4*_6d3nl74ayu-r%@#8j+66@w2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

import djcelery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest:guest@localhost:5672//'

CELERY_RESULT_BACKEND = 'amqp' # very important for getting results

CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


# Application definition

INSTALLED_APPS = [
    'coreapp',
    'captcha', # Include the django-simple-captcha application
    'rest_framework',
    # 'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'multiselectfield',
    'djcelery'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dua.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
	    # insert your TEMPLATE_DIRS here
            os.path.join(BASE_DIR, 'templates')
	],
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

WSGI_APPLICATION = 'dua.wsgi.application'


# Database

# Define the database manager to setup the various projects
# DATABASE_ROUTERS = ['manager.router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {#'default': 'client', # default we neednot specify
                         # 'T50_VATC':'t50_db'
                         }


_MONGODB_USER = 'mongouser'
_MONGODB_PASSWD = 'password'
_MONGODB_HOST = 'thehost'
_MONGODB_NAME = 'thedb'
_MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s/%s' \
    % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)

# mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)
mongoengine.connect('test', host='mongodb://localhost:27017/')

# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # 'mongodb':{
    #     'ENGINE' : 'django_mongodb_engine',
    #     'NAME' : 'db'
    # }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/coreapp/static/',
]

MONGO_URL = 'mongodb://52.11.209.17:27017/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aakashnln11.4@gmail.com'
EMAIL_HOST_PASSWORD = '86245301'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'aakashnln11.4@gmail.com'
