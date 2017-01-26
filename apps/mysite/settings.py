"""
Django settings for apps project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from mongoengine import connect


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')%snqj97hc5=-(v8sm!$j#x+t+&!mchm&8f2s03!%szg6ysv+k'

# SECURITY WARNING: don't run with debug turned on in productoin!
DEBUG = True

DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'bethel_core.apps.BethelcoreConfig',
    'cell.apps.CellsConfig',
    'cell_metting.apps.CellmettingsConfig',    
    'user.apps.UsersConfig',
    'overview.apps.OverviewConfig',
    'mig.apps.MigConfig',    

    'rest_framework_mongoengine',
    'rest_framework',

    'oauth2_provider',
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES =[
]

MIDDLEWARE_CLASSES = [
    #'django_pudb.PudbMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'bethel_core.middleware.auth.BethelAuth'
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',    
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bethel_core.context_processors.my_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
        'NAME': '/tmp/apps.sqlite3',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': os.path.join('/home/douglas/work/docker/bethelauth/db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


#LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'bethel_core/log/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'pt_BR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


#Mongo DB
from mongoengine import connect
connect('betheldb', username='mongodb')


TEST_MONGO_DATABASE = {
    'db': 'test',
    'host': ['localhost'],
    'port': 27017,
}



CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:10',
        'OPTIONS': {
            'DB': 0,
        },
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"


SESSION_COOKIE_PATH = '/;HttpOnly'
SESSION_COOKIE_NAME = 'abracadabra'


#CSRF_COOKIE_HTTPONLY = True
#CSRF_COOKIE_NAME = 'honda_csrf_230'


#CORS_ORIGIN_WHITELIST = (
#    'localhost:81',
#)
CORS_ORIGIN_ALLOW_ALL = True


# Bethelgroups Settings
#Base url WITHOUT end slash "/""
BASE_URL = 'http://localhost:10'

#Default Login URL
LOGIN_URL = BASE_URL+'/login'

#Default 403 template
FORBIDDEN_PAGE = BASE_URL+'/errou'


AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
)

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )    
}