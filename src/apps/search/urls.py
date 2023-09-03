from django.urls import path

from .views import ArticleElasticsearchView

urlpatterns = [
    path("", ArticleElasticsearchView.as_view({"get": "list"}), name="article-search"),
]
