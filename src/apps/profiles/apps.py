from django.apps import AppConfig
from django.utils.translation import gettext_lazy as t


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.profiles"
    verbose_name = t("Profile")
    verbose_name_plural = t("Profiles")
