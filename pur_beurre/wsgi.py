"""
WSGI config for pur_beurre project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pur_beurre.settings')

application = get_wsgi_application()

user_name = os.environ.get('USER')
SECRET_KEY = os.environ.get('SECRET_KEY')

