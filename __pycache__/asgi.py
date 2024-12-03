"""
ASGI config for meu_projeto project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Define a configuração do ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')

# Cria e expõe o objeto de aplicação ASGI
application = get_asgi_application()
