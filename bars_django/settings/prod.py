from .common import *

ALLOWED_HOSTS = [
    "chocapix",
    "chocapix.bin",
    "chocapix.binets.fr",
    "chocapix.eleves.polytechnique.fr",
    "bars.nadrieril.fr"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'HOST': 'mysqldb',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}
