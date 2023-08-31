from django.apps import AppConfig
from django.utils.translation import gettext_lazy as t


class RatingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.ratings"
    verbose_name = t("Ratings")
