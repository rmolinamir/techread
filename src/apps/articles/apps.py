from django.apps import AppConfig
from django.utils.translation import gettext_lazy as t


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.articles"
    verbose_name = t("Articles")

    # Let Django know about the signals that we created in the signals.py file.
    def ready(self):
        from src.apps.search import signals  # noqa
