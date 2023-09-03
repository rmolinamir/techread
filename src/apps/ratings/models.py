from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as t

from src.apps.articles.models import Article
from src.apps.common.models import BaseEntityModel

User = get_user_model()


class Rating(BaseEntityModel):
    class Meta:
        unique_together = ("article", "user")
        verbose_name = t("Rating")
        verbose_name_plural = t("Ratings")

    RATING_CHOICES = (
        (1, "Poor"),
        (2, "Fair"),
        (3, "Good"),
        (4, "Very Good"),
        (5, "Excellent"),
    )
    article = models.ForeignKey(Article, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} rated {self.article.title} as {self.get_rating_display()}"
