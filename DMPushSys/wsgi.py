"""
WSGI config for DMPushSys project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from DMPush.apifunction import startSched, send_all
from DMPush.models import Product
from DMPushSys.settings import sched

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DMPushSys.settings")

application = get_wsgi_application()
startSched()
