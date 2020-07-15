"""
Django settings for tools_app project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import re
import tools_app.git


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WWW_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
LOG_DIR = os.path.join(os.environ.get('HOME'), 'logs')
VERSION_ID = tools_app.git.get_info()


# Intuit our toolforge tool name from the file system path.
m = re.match(r'.*/(?P<tool_name>[^/]*)/www/python/src', BASE_DIR)
if not m:
    raise RuntimeError("BASE_DIR doesn't make sense: %s" % BASE_DIR)
TOOL_NAME = m.group('tool_name')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'tools.wmflabs.org',
    'spi-tools-dev.toolforge.org',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cat_checker',
    'spi',
    'pageutils',
    'tools_app',
    'social_django',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'tools_app.middleware.LoggingMiddleware',
]

ROOT_URLCONF = 'tools_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'tools_app.context_preprocessors.debug',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.mediawiki.MediaWiki',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_MEDIAWIKI_KEY = os.environ.get('MEDIAWIKI_KEY')
SOCIAL_AUTH_MEDIAWIKI_SECRET = os.environ.get('MEDIAWIKI_SECRET')
SOCIAL_AUTH_MEDIAWIKI_URL = 'https://meta.wikimedia.org/w/index.php'
SOCIAL_AUTH_MEDIAWIKI_CALLBACK = 'https://%s.toolforge.org/oauth/complete/mediawiki/' % TOOL_NAME

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'

WSGI_APPLICATION = 'tools_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files setup.  For more information, see:
#   https://wikitech.wikimedia.org/wiki/Portal:Toolforge/Tool_Accounts
#   https://docs.djangoproject.com/en/2.2/howto/static-files
if DEBUG:
    STATIC_URL = f'/{TOOL_NAME}/static/'
else:
    STATIC_URL = f'//tools-static.wmflabs.org/{TOOL_NAME}/'
    STATIC_ROOT = f'{WWW_DIR}/static/'
    FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o711

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: False,
    }

if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'django.log'),
            },
            # Hack to get real-time logging, as a work-around to T256426 and T256482.
            'bastion': {
                'level': 'DEBUG',
                'class': 'logging.handlers.SocketHandler',
                'host': 'tools-sgebastion-08.tools.eqiad.wmflabs',
                'port': 23001,
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file', 'bastion'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'view': {
                'handlers': ['file', 'bastion'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
