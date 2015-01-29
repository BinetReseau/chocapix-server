from .common import *

# TODO : temporary
DEBUG = True
TEMPLATE_DEBUG = True

STATIC_URL = '/bars/api/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'HOST': 'mysql',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}
