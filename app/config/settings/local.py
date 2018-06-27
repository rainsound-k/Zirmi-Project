from .base import *

secrets = json.loads(open(SECRETS_LOCAL, 'rt').read())
set_config(secrets, module_name=__name__, start=True)

DEBUG = True

ALLOWED_HOSTS = ['localhost']
INSTALLED_APPS += [
    'django_extensions',
]

WSGI_APPLICATION = 'config.wsgi.local.application'


