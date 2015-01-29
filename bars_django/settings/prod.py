from .common import *

# TODO : temporary
DEBUG = True
TEMPLATE_DEBUG = True
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.AllowAny',
]


INSTALLED_APPS = INSTALLED_APPS + (
    'django.contrib.staticfiles',
    'django_extensions',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'HOST': 'mysqldb',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}
