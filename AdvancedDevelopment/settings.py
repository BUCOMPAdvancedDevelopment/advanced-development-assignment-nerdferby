"""
Django settings for AdvancedDevelopment project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
import djongo
import requests
from google.api_core.exceptions import PermissionDenied
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import secretmanager

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
secrets = secretmanager.SecretManagerServiceClient()
SECRET_KEY = secrets.access_secret_version(
        name="projects/idyllic-kit-328813/secrets/django_secret_key/versions/latest")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "idyllic-kit-328813.ew.r.appspot.com"]

# Application definition

INSTALLED_APPS = [
    'address',
    'products.apps.ParcelConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AdvancedDevelopment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + 'templates'],
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

WSGI_APPLICATION = 'AdvancedDevelopment.wsgi.application'

# Use Bootstrap 4 Forms With Django
# https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Certifying Firebase credentials for Firebase integration
# https://jrizmal.medium.com/how-to-authenticate-firebase-users-in-django-rest-framework-c2d90f5a0a11

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'FirebaseAuth.authentication.FirebaseAuthentication',
#     ]
# }

# Specify your Google API key as environment variable GOOGLE_API_KEY
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, "firebase_admin_sdk.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
                                                              GOOGLE_APPLICATION_CREDENTIALS)

# try:
#     # todo save response to file
#     response = secrets.access_secret_version(
#         name="projects/idyllic-kit-328813/secrets/Firebase_Admin_SDK/versions/latest")
#     cred = credentials.Certificate(response)
# except PermissionDenied as exception:  # todo write to log
#     cred = credentials.Certificate(os.path.join(BASE_DIR, "firebase_admin_sdk.json"))
#
# firebase_admin.initialize_app(cred)
