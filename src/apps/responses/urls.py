from django.urls import path

from .views import ResponseListCreateView, ResponseUpdateDeleteView

urlpatterns = [
    path(
        "<uuid:article_id>/",
        ResponseListCreateView.as_view(),
        name="response-list-create",
    ),
    path(
        "<uuid:article_id>/<uuid:id>",
        ResponseUpdateDeleteView.as_view(),
        name="response-update-delete",
    ),
]
