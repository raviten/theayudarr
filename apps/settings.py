# -*- coding: utf-8 -*-
"""
Django settings for apps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9j#f(u6tpi*o#$6l*8&)%^15%n_$uuiuii)4y-dd@flv5!&!ic'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

#AUTH_USER_MODEL = 'theayudar.models.l'


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'theayudar',
#    'contacts',
)


AUTHENTICATION_BACKENDS = ('backends.EmailAuthBackend',)

SESSION_ENGINE='django.contrib.sessions.backends.cache'
    

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',#enables session support
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',#cross site request forgery required while using post method from client
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',#enables cookie and session based messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',#enbles protection against cross site request forgery
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
)

ROOT_URLCONF = 'apps.urls'

WSGI_APPLICATION = 'apps.wsgi.application'

##//docs.djangoproject.com/en/1.6/ref/settings/#databases

##DATABASES = {
##    'default': {
##        'ENGINE': 'django.db.backends.sqlite3',
##        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
##    }
##}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoazure',               
        'USER': 'testazureuser',  
        'PASSWORD': 'testazure',
        'HOST': '127.0.0.1', 
        'PORT': '3306',
    },
        'theayudar': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'ayudar',
        'USER': 'ayudar',
        'PASSWORD': 'ayudar123',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
##Dont use thisfor time bieng
##STATICFILES_DIRS = (
##    os.path.join(os.path.dirname(__file__), "static")
##)
##Caches used in application
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
                '127.0.0.1:11211',
##                '127.0.0.1:11212',
                ]
    }
   
}




LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "F:/wad/apps/theayudar/logs/debug.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'theayudar': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}




