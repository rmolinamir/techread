from django.apps import AppConfig
from django.utils.translation import gettext_lazy as t


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.common"
    verbose_name = t("Common")
    verbose_name_plural = t("Common")
