"""
WSGI config for webluxe project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Añadir la ruta a tu proyecto
sys.path.append('/var/www/html/webluxe')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webluxe.settings')

application = get_wsgi_application()
