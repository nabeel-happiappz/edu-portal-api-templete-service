"""
ASGI config for portal_api project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_api.settings')

application = get_asgi_application()
