"""
Django settings for wis-application project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from mongoengine import *
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DEBUG = True
TEMPLATE_DEBUG = True


# ADMINS: receive emails during errors if DEBUG=False
ADMINS = (
    ('Sameen Karim', 'sameenkarim@gmail.com'),
)


# ALLOWED HOSTS: which domains to allow to run on
if not DEBUG:
    ALLOWED_HOSTS = [
        'wis-application',
        'application.mcawis.org',
    ]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rvW2yT9GB3HKB1eTv3gd63LcMdIebfCKDCjTXKssme7NgC7ZTZ'


# MONGO DB: ignore django ORM and use mongoengine
DBNAME = 'wis_coredata'
connect(DBNAME, tz_aware=True)


# Application definitions
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custom apps
    'authorization',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'wis-application.urls'


WSGI_APPLICATION = 'wis-application.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'


# Database (IGNORED)
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'django',
#         'USER': 'django',
#         'PASSWORD': 'tn1sHlDzJo',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }