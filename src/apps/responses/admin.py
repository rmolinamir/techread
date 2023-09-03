from django.contrib import admin

from .models import Response


class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        "_id",
        "id",
        "article",
        "user",
        "parent_response",
        "content",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "article", "user", "parent_response")
    search_fields = ("article", "user")
    list_per_page = 25


admin.site.register(Response, ResponseAdmin)
