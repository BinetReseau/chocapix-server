from .dev_local import *

STATIC_URL = '/bars/api/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}
