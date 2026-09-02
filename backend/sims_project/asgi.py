"""
ASGI config for sims_project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/

SIMS - Postgraduate Medical Training System
Created: 2025-05-29 16:07:19 UTC
Author: SMIB2012
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

application = get_asgi_application()