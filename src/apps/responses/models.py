from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as t
from src.apps.common.models import BaseEntityModel
from src.apps.articles.models import Article

User = get_user_model()


class Response(BaseEntityModel):
    class Meta:
        verbose_name = t("Response")
        verbose_name_plural = t("Responses")
        ordering = ("-created_at",)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="responses"
    )
    parent_response = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )
    content = models.TextField(verbose_name=t("Response Content"))

    def __str__(self) -> str:
        return f"{self.user.first_name} commented on {self.article.title}"
