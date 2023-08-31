from .base import *  # noqa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="WneRPSDeZKXcTAIjvQa1DTTyY4L7L3o6CHJwNJ2SwoCaWAIxA5E"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

# Celery configuration.
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT", default=1025)
DEFAULT_FROM_EMAIL = "no-reply@techread.site"
DOMAIN = env("DOMAIN")
SITE_NAME = "TechRead"
