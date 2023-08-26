from django.apps import AppConfig
from django.utils.translation import gettext_lazy as t


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.users"
    verbose_name = t("User")
    verbose_name_plural = t("Users")
