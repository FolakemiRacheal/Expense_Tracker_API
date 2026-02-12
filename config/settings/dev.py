from .base import *

# Development settings
DEBUG = True

SECRET_KEY = 'django-insecure-rqwhq5uupy&an)zkab2s5+%1w*y7ki5p082%w9q@w69efmh%6_'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Development-specific apps
# INSTALLED_APPS += [
#     'django_extensions',  # Optional: for shell_plus, etc.
# ]