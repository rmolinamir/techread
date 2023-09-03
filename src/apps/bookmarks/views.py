from django.db import IntegrityError
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from src.apps.articles.models import Article
from src.apps.bookmarks.exceptions import ArticleAlreadyBookmarked

from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkCreateView(generics.CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")

        if not article_id:
            raise ValidationError("Article ID is required.")

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise ValidationError("Article does not exist.")

        try:
            serializer.save(article=article, user=self.request.user)
        except IntegrityError:
            raise ArticleAlreadyBookmarked


class BookmarkDestroyView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    lookup_field = "article_id"
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        article_id = self.kwargs.get("article_id")
        try:
            return Bookmark.objects.get(article__id=article_id, user=user)
        except Bookmark.DoesNotExist:
            raise ValidationError("Bookmark does not exist.")

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.user != user:
            raise ValidationError("You cannot delete this bookmark.")
        else:
            instance.delete()
