from django.contrib import admin
from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "user", "created_at", "updated_at")
    list_display_links = ("id", "article", "user")
    search_fields = ("article", "user")
    list_per_page = 25


admin.site.register(Bookmark, BookmarkAdmin)
