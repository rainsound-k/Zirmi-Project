"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import importlib
import json
import numbers
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')
SECRETS_LOCAL = os.path.join(SECRETS_DIR, 'local.json')
SECRETS_DEV = os.path.join(SECRETS_DIR, 'dev.json')
SECRETS_PRODUCTION = os.path.join(SECRETS_DIR, 'production.json')

secrets = json.loads(open(SECRETS_BASE, 'rt').read())


def set_config(obj, module_name=None, start=False):
    def eval_obj(obj):
        # 객체가 int, float거나
        if isinstance(obj, numbers.Number) or (
                # str형이면서 숫자 변환이 가능한 경우
                isinstance(obj, str) and obj.isdigit()):
            return obj

        # 객체가 int, float가 아니면서 숫자형태를 가진 str도 아닐경우
        try:
            return eval(obj)
        except NameError:
            # 없는 변수를 참조할 때 발생하는 예외
            return obj
        except Exception as e:
            print(f'Cannot eval object({obj}), Exception: {e}')
            return obj
            # raise ValueError(f'Cannot eval object({obj}), Exception: {e}')

    # base.json파일을 parsing한 결과 (Python dict)를 순회
    # set_config에 전달된 객체가 'dict'형태일 경우
    if isinstance(obj, dict):
        # key, value를 순회
        for key, value in obj.items():
            # value가 dict거나 list일 경우 재귀적으로 함수를 다시 실행
            if isinstance(value, dict) or isinstance(value, list):
                set_config(value)
            # 그 외의 경우 value를 평가한 값을 할당
            else:
                obj[key] = eval_obj(value)
            # set_config()가 처음 호출된 loop에서만 setattr()을 실행
            if start:
                setattr(sys.modules[module_name], key, value)
    # 전달된 객체가 'list'형태일 경우
    elif isinstance(obj, list):
        # list아이템을 순회하며
        for index, item in enumerate(obj):
            # list의 해당 index에 item을 평가한 값을 할당
            obj[index] = eval_obj(item)


setattr(sys.modules[__name__], 'raven', importlib.import_module('raven'))
set_config(secrets, module_name=__name__, start=True)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]

AUTH_USER_MODEL = 'members.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.FacebookBackend',  # Facebook Backend
    'members.backends.APIFacebookBackend',  # API Facebook
]

# REST_FRAMEWORK 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # integerfield 천단위로 콤마 구분

    'django_summernote',
    'django_filters',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',

    'items',
    'members',
    'reviews',
    'utils',
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

ROOT_URLCONF = 'config.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
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

# django_summernote(wysiwyg) 관련 설정
SUMMERNOTE_CONFIG = {
    'summernote': {
        'airMode': False,
        'width': '100%',
        'height': '520',
        'lang': 'ko-KR',
    },
    'base_css': (
        '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
    ),
    'base_js': (
        '//code.jquery.com/jquery-3.2.1.min.js',
        '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
    ),

    # Media files for CodeMirror
    'codemirror_css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/codemirror.min.css',
    ),
    'codemirror_js': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/codemirror.min.js',
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/mode/xml/xml.min.js',
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/mode/htmlmixed/htmlmixed.min.js',
    ),

    # Media files for all Summernote widgets
    'default_css': (
        'summernote/summernote.css',
        'summernote/django_summernote.css',
    ),
    'default_js': (
        'summernote/jquery.ui.widget.js',
        'summernote/jquery.iframe-transport.js',
        'summernote/jquery.fileupload.js',
        'summernote/summernote.min.js',
        'summernote/ResizeSensor.js',
    ),
}

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False
