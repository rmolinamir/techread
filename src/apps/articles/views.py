import logging

from django.http import Http404
from rest_framework.response import Response
from rest_framework import filters, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Article, ArticleView
from .serializers import ArticleSerializer
from .filters import ArticleFilter
from .pagination import ArticlePagination
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .permissions import IsAuthorOrReadOnly

User = get_user_model()

logger = logging.getLogger(__name__)


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = ArticlePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ArticleFilter
    ordering_fields = (
        "created_at",
        "updated_at",
    )
    renderer_classes = (ArticlesJSONRenderer,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(
            f"Article {serializer.data.get('title')} created by {self.request.user.first_name}"
        )


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)
    lookup_field = "id"
    renderer_classes = (ArticleJSONRenderer,)
    parser_classes = (MultiPartParser, FormParser)

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)

        if "banner_image" in self.request.FILES:
            # Delete old banner image if it exists.
            if (
                instance.banner_image
                and "default_photos" not in instance.banner_image.url
            ):
                default_storage.delete(instance.banner_image.path)

            instance.banner_image = self.request.FILES.get("banner_image")
            instance.save()

    def retrieve(self, request, *args, **kwargs):
        try:
            article = self.get_object()
            viewer_ip = self.request.META.get("REMOTE_ADDR")
            ArticleView.record_view(
                article=article, user=request.user, viewer_ip=viewer_ip
            )
            serializer = self.get_serializer(article)
            return Response(serializer.data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
