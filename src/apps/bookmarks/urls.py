from django.urls import path

from .views import BookmarkCreateView, BookmarkDestroyView

urlpatterns = [
    path(
        "bookmark/<uuid:article_id>/",
        BookmarkCreateView.as_view(),
        name="bookmark-create",
    ),
    path(
        "bookmark/<uuid:article_id>/delete/",
        BookmarkDestroyView.as_view(),
        name="bookmark-delete",
    ),
]
