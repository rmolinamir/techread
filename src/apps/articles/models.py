from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as t
from taggit.managers import TaggableManager
from src.apps.common.models import BaseEntityModel
from .read_time_engine import ArticleReadTimeEngine

User = get_user_model()


# Create your models here.
class Article(BaseEntityModel):
    class Meta:
        verbose_name = t("Article")
        verbose_name_plural = t("Articles")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(verbose_name=t("Title"), max_length=255)
    slug = AutoSlugField(
        populate_from="title", always_update=True, unique=True, editable=False
    )
    body = models.TextField(verbose_name=t("Article Content"))
    banner_image = models.ImageField(verbose_name=t("Banner Image"))
    tags = TaggableManager(verbose_name=t("Tags"))

    def __str__(self):
        return f"${self.author.first_name}'s Article: {self.title}"

    @property
    def estimated_reading_time(self):
        return ArticleReadTimeEngine(self).estimate_reading_time()

    def view_count(self):
        return self.article_views.count()


class ArticleView(BaseEntityModel):
    class Meta:
        verbose_name = t("Article View")
        verbose_name_plural = t("Article Views")

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_views"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="article_views"
    )
    viewer_ip = models.GenericIPAddressField(
        verbose_name=t("Viewer IP"), null=True, blank=True
    )

    def __str__(self):
        if self.user:
            return f"{self.user.first_name}'s View of {self.article.title}"
        else:
            return f"Anonymous View of {self.article.title}"

    @classmethod
    def record_view(cls, article, user, viewer_ip):
        view, created = cls.objects.get_or_create(
            article=article, user=user, viewer_ip=viewer_ip
        )
        view.save()
