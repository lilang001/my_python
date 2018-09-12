# -*- coding: utf-8 -*-
"""
if you want see settings in old version, please see ./bak_settings.py
"""

import socket
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# Build paths inside the project like this: os.path.join(PROJECT_ROOT, ...)

import os

PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir).replace('\\', '/')

# app and lib settings
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_r&eypnc%rp1f5slops98fwqayc0!ze_nb^06g55%2^9)hq049'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# ALLOWED_HOSTS = ['localhost', '192.168.1.164']

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.16', 'maiziedu142.com', 'jackie.maiziedu.com']

TEMPLATE_DEBUG = DEBUG

# template setting
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates").replace('\\', '/'),
    os.path.join(PROJECT_ROOT, 'apps', 'mz_plus', 'templates').replace('\\', '/'),
    os.path.join(PROJECT_ROOT, 'apps', 'mz_crawl', 'templates').replace('\\', '/'),
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'mz_course',
    'mz_plus',
    "mz_crawl",
)

MIDDLEWARE_CLASSES = (
)

# 共用上下文处理器定义
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'maiziedu_website.urls'

WSGI_APPLICATION = 'maiziedu_website.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lps_1106',
        'USER': 'root',
        'PASSWORD': '1234',
        # 'HOST': '192.168.1.142',
        'HOST': 'local_vhost',
        'PORT': '',
    },
    'crawl': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crawl_1027',
        'USER': 'root',
        'PASSWORD': '1234',
        # 'HOST': '192.168.1.142',
        'HOST': 'local_vhost',
        'PORT': '',
    },
}

# Internationalization

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i'
TIME_FORMAT = 'H:i'

# 静态文件地址映射
STATIC_URL = '/static/'

# 关闭调试模式之后需开启STATIC_ROOT设置才能正确加载静态文件
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static').replace('\\', '/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# 媒体地址映射
MEDIA_URL = 'http://www.maiziedu.com/uploads/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads').replace('\\', '/')


# from django.conf import global_settings
DATABASE_ROUTERS = ['mz_crawl.router.CrawlDBRouter']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
import logging

logging.basicConfig(format='%(asctime)s %(message)s ---------- %(pathname)s:%(module)s.%(funcName)s Line:%(lineno)d',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)
