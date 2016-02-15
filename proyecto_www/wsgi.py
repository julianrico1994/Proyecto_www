"""
WSGI config for proyecto_www project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

#from dj_static import Cling



#For deployment
try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto_www.settings.staging")
    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(get_wsgi_application())
except:
#For development
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto_www.settings.local")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

