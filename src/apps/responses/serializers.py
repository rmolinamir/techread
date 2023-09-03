from rest_framework import serializers

from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            "_id",
            "id",
            "article_title",
            "user_first_name",
            "user_last_name",
            "parent_response",
            "content",
            "created_at",
        ]

    article_title = serializers.CharField(source="article.title", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)
