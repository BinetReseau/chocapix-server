"""
WSGI config for bars_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))));
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bars_django.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
