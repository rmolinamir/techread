"""techread URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from dj_rest_auth.views import PasswordResetConfirmView
from src.apps.users.views import UserDetailsView

schema_view = get_schema_view(
    openapi.Info(
        title="TechRead API",
        default_version="v1",
        description="API for TechRead",
        contact=openapi.Contact(email="rmolinamir@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
    # Auth URLs
    path("api/v1/auth/user/", UserDetailsView.as_view(), name="user_details"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "api/v1/auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # Profiles URLs
    path("api/v1/profiles/", include("src.apps.profiles.urls")),
    # Articles URLs
    path("api/v1/articles/", include("src.apps.articles.urls")),
    # Ratings URLs
    path("api/v1/ratings/", include("src.apps.ratings.urls")),
]

admin.site.site_header = "TechRead Admin"
admin.site.site_title = "TechRead Admin Portal"
admin.site.index_title = "Welcome to the TechRead Admin Portal"
