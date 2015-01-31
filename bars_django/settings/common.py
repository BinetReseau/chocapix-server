"""
Django settings for bars_django project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')$w@s+3e_&cl19@c2-qbi^rr6fnzj4p*0%3u_xtltj0*-cc0&v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'corsheaders',
    'permission',
    'bars_api',
)


MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bars_django.urls'

WSGI_APPLICATION = 'bars_django.wsgi.application'

ATOMIC_REQUESTS = True

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/api/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')

# Rest framework

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.AllowAny',
        # 'bars_api.perms.PerBarPermissionsOrAnonReadOnly',
        'rest_framework.permissions.DjangoObjectPermissions',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # TODO: remove
        'rest_framework.authentication.BasicAuthentication',  # TODO: remove
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter'
    )
}

AUTHENTICATION_BACKENDS = (
    'bars_api.auth.AuthenticationBackend',
    'bars_api.perms.BarPermissionBackend',
    'permission.backends.PermissionBackend',
)

import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=7 * 24),  # Todo: temporary
}

# Permissions

PERMISSION_CHECK_PERMISSION_PRESENCE = False
PERMISSION_DEFAULT_APL_ANY_PERMISSION = False
PERMISSION_DEFAULT_APL_CHANGE_PERMISSION = True
PERMISSION_DEFAULT_APL_DELETE_PERMISSION = False

# CORS headers

CORS_ORIGIN_ALLOW_ALL = True


# API app

AUTH_USER_MODEL = 'bars_api.User'
