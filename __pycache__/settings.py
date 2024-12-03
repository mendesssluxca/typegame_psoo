DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'game_psoo',  # Nome do banco de dados criado no pgAdmin
        'USER': 'postgres',          # Usuário do PostgreSQL
        'PASSWORD': '123456',     # Senha do usuário do PostgreSQL
        'HOST': 'localhost',         # Se estiver no mesmo computador
        'PORT': '5432',              # Porta padrão do PostgreSQL
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Adicione este caso esteja usando o Django Rest Framework
    'jogo_rank',  # Certifique-se de que seu aplicativo está aqui
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
