from django.apps import AppConfig
from django.utils.translation import gettext_lazy as t


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.profiles"
    verbose_name = t("Profile")
    verbose_name_plural = t("Profiles")

    # Let Django know about the signals that we created in the signals.py file.
    def ready(self):
        from src.apps.profiles import signals  # noqa
