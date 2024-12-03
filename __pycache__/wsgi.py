import os
from django.core.wsgi import get_wsgi_application

# Defina o ambiente para o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')

# Crie a aplicação WSGI
application = get_wsgi_application()
