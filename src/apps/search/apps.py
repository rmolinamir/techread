from django.apps import AppConfig
from django.utils.translation import gettext_lazy as t


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.search"
    verbose_name = t("Search")
    verbose_name_plural = t("Searches")
