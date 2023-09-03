from django.apps import AppConfig
from django.utils.translation import gettext_lazy as t


class ResponsesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.responses"
    verbose_name = t("Response")
    verbose_name_plural = t("Responses")
