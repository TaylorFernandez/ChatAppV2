from chat.settings.common import *
# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-10^i-7!$ump155e9(07j7%a5h6ux)48-rw-6@ve3o&1%1r+q9b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'db.sqlite3',
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}