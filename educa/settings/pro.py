from .base import *
import os
DJANGO_ALLOWED_HOSTS=os.environ.get("DJANGO_ALLOWED_HOSTS","*").split(" ")
SECRET_KEY = os.environ.get("SECRET_KEY")
ADMINS = (
    (os.environ.get('ADMIN_USERNAME',''), os.environ.get('ADMIN_EMAIL','email@mydomain.com')),
)
DEBUG = int(os.environ.get("DEBUG", default=0))
DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.postgresql',
        'NAME':os.environ.get("DB_NAME", "educa"),
        'USER':os.environ.get("DB_USER", "postgres"),
        'PASSWORD':os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432")
    }
}
CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels_redis.core.RedisChannelLayer',
        'CONFIG':{
            'hosts':[('redis', 6379)],
        }
    }
}
