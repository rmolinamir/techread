from django.db import IntegrityError
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from src.apps.articles.models import Article
from src.apps.ratings.exceptions import ArticleAlreadyRated

from .models import Rating
from .serializers import RatingSerializer


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
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
            raise ArticleAlreadyRated
