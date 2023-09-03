from django.contrib import admin

from .models import Article, ArticleView, Clap


class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "_id",
        "id",
        "author",
        "title",
        "slug",
        "view_count",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["_id", "id", "author"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "body", "tags"]
    ordering = ["-created_at"]


class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ["_id", "article", "user", "viewer_ip"]
    list_display_links = ["_id", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]
    ordering = ["-created_at"]


class ClapAdmin(admin.ModelAdmin):
    list_display = ["_id", "article", "user", "count"]
    list_display_links = ["_id", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user"]
    ordering = ["-created_at"]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleView, ArticleViewAdmin)
admin.site.register(Clap, ClapAdmin)
