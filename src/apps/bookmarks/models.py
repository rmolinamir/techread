from django.contrib.auth import get_user_model
from django.db import models

from src.apps.articles.models import Article
from src.apps.common.models import BaseEntityModel

User = get_user_model()


class Bookmark(BaseEntityModel):
    class Meta:
        unique_together = ("article", "user")
        ordering = ("-created_at",)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="bookmarks")

    def __str__(self) -> str:
        return f"{self.user.first_name} bookmarked {self.article.title}"
