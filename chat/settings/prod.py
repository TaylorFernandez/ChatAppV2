from chat.settings.common import *
from dotenv import load_dotenv
from os import environ
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent.parent / "prod.env")
# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", None).split(',')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get("DJANGO_SECRET_KEY", None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get("PG_NAME", "root"),
        'USER': environ.get("PG_USER", "root"),
        'PASSWORD': environ.get("PG_PASS", "root"),
        'HOST': environ.get("PG_HOST", "localhost"),
        'PORT': environ.get("PG_PORT", "5432"),
    }
}

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }
#We'll use in memory channel layer for now since redis technically isn't required yet. 
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}