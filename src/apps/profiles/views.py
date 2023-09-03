# TODO: Change this in production
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.project.settings.local import DEFAULT_FROM_EMAIL

from .exceptions import NoFollowingYourself, NoUnfollowingYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = (ProfilesJSONRenderer,)


class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)

    def get_queryset(self):
        # `select_related` efficiently selects related user and profile
        # because this only executes a single database query.
        return Profile.objects.select_related("user")

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileAPIView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    # MultiPartParser allows us to send files such as images in our request.
    parser_classes = (MultiPartParser,)

    def get_object(self):
        return self.request.user.profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": follower_profiles.count(),
                "followers": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"error": "You don't have a profile yet."},
                status=status.HTTP_404_NOT_FOUND,
            )


class FollowingListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user_id = request.GET.get("user_id")
            profile = Profile.objects.get(user__id=user_id)
            following_profiles = profile.following.all()
            serializer = FollowingSerializer(following_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "following_count": following_profiles.count(),
                "following": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"error": "You don't have a profile yet."},
                status=status.HTTP_404_NOT_FOUND,
            )


class FollowAPIView(APIView):
    def post(self, request, user_id, format=None):
        try:
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)

            if user_profile == profile:
                raise NoFollowingYourself()

            if user_profile.is_following(profile):
                formatted_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are already following {profile.user.first_name} {profile.user.last_name}",
                }
                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

            user_profile.follow(profile)

            subject = "A new user follows you!"
            message = (
                f"Hi {profile.user.first_name},\n\n"
                f"{user_profile.user.first_name} {user_profile.user.last_name} is now following you on TechRead!"
            )
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [profile.user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": f"You are now following {profile.user.first_name} {profile.user.last_name}",
                }
            )
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist.")


class UnfollowAPIView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        user_profile = request.user.profile
        profile = Profile.objects.get(user__id=user_id)

        if user_profile == profile:
            raise NoUnfollowingYourself()

        if not user_profile.is_following(profile):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"You are not following {profile.user.first_name} {profile.user.last_name}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        user_profile.unfollow(profile)

        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "message": f"You have unfollowed {profile.user.first_name} {profile.user.last_name}",
        }

        return Response(formatted_response, status=status.HTTP_200_OK)
