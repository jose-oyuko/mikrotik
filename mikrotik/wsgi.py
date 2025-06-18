"""
WSGI config for mikrotik project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# logger 
from mikrotikapp.utils import setup_logging
setup_logging()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mikrotik.settings")

application = get_wsgi_application()
