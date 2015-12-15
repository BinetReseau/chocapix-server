from .common import *

ALLOWED_HOSTS = [
    "localhost",
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

EMAIL_HOST = "frankiz"
EMAIL_PORT = 25

ADMINS = (("Babe", "babe@eleves.polytechnique.fr"),)
SERVER_EMAIL = 'root@chocapix.eleves.polytechnique.fr'

SLACK_HOOK = True
# Kuzh - for Slack hook requests
PROXIES = {
    "http": "http://129.104.247.2:8080/",
    "https": "http://129.104.247.2:8080/"
}
