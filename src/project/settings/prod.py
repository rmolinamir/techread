from .base import *  # noqa
from .base import env

# Django will email error details to the listed contacts when `DEBUG` is `False`.
ADMINS = [("Robert Molina", "rmolinamir@gmail.com")]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="WneRPSDeZKXcTAIjvQa1DTTyY4L7L3o6CHJwNJ2SwoCaWAIxA5E"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# TODO: Setup production domain names.
CSRF_TRUSTED_ORIGINS = [""]
