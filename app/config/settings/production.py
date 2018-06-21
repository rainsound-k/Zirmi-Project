from .base import *

secrets = json.loads(open(SECRETS_PRODUCTION, 'rt').read())
set_config(secrets, module_name=__name__, start=True)

DEBUG = False
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.elasticbeanstalk.com',
]
WSGI_APPLICATION = 'config.wsgi.production.application'
INSTALLED_APPS += [
    # 'storages',
]

# S3대신 EC2에서 정적파일을 제공 (프리티어 put 사용량 절감)
# DEFAULT_FILE_STORAGE = 'config.storage.DefaultFileStorage'
STATICFILES_STORAGE = 'config.storage.StaticFilesStorage'
