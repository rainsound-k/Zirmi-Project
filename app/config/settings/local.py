from .base import *

SECRET_KEY = secrets_base['SECRET_KEY']
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS += [
    'django_extensions',
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
