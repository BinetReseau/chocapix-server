from .common import *

DEBUG = True

TEMPLATE_DEBUG = True


INSTALLED_APPS = INSTALLED_APPS + (
    'django.contrib.staticfiles',
    'django_extensions',
    # 'debug_toolbar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'django',
        # 'HOST': '127.0.0.1',
        # 'USER': 'root',
        # 'PASSWORD': 'root',
        # 'PORT': 3306
    }
}

# DEBUG_TOOLBAR_PATCH_SETTINGS = False  #Bugfix


# # Debug
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
#         },
#     },
#     'handlers': {
#         'default': {
#             'level':'DEBUG',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename': '/var/www/logs/python.log',
#             'maxBytes': 1024*1024*5, # 5 MB
#             'backupCount': 5,
#             'formatter':'standard',
#         },
#         'request_handler': {
#                 'level':'DEBUG',
#                 'class':'logging.handlers.RotatingFileHandler',
#                 'filename': '/var/www/logs/django_request.log',
#                 'maxBytes': 1024*1024*5, # 5 MB
#                 'backupCount': 5,
#                 'formatter':'standard',
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['default'],
#             'level': 'DEBUG',
#             'propagate': True
#         },
#         'django.request': {
#             'handlers': ['request_handler'],
#             'level': 'DEBUG',
#             'propagate': True
#         },
#     }
# }
