from django.urls import path

from .views import (
    FollowAPIView,
    FollowerListView,
    FollowingListView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    UnfollowAPIView,
    UpdateProfileAPIView,
)

urlpatterns = [
    path("", ProfileDetailAPIView.as_view(), name="my-profile"),
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path("update/", UpdateProfileAPIView.as_view(), name="update-profile"),
    path("followers/", FollowerListView.as_view(), name="followers"),
    path("following/", FollowingListView.as_view(), name="following"),
    path("<uuid:user_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
]
