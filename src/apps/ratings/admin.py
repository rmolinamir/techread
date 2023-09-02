from django.contrib import admin
from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "user", "rating", "created_at", "updated_at")
    list_display_links = ("id", "article", "user")
    search_fields = ("article", "user", "rating")
    list_per_page = 25


admin.site.register(Rating, RatingAdmin)
