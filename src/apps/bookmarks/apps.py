from django.apps import AppConfig
from django.utils.text import gettext_lazy as t


class BookmarksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.bookmarks"
    verbose_name = t("Bookmark")
