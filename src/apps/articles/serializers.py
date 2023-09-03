from rest_framework import serializers
from src.apps.profiles.serializers import ProfileSerializer
from src.apps.responses.serializers import ResponseSerializer
from src.apps.bookmarks.models import Bookmark
from .models import Article, ArticleView, Clap


class TagListField(serializers.Field):
    def to_representation(self, value):
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError(
                "Expected a list of tags but got type '%s'." % type(data).__name__
            )

        tags = []

        for tag_name in data:
            tag_name = tag_name.strip()
            if tag_name:
                tags.append(tag_name)

        return tags


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "tags",
            "estimated_reading_time",
            "author_info",
            "views",
            "average_rating",
            "claps_count",
            "bookmarks",
            "responses",
            "responses_count",
            "description",
            "body",
            "banner_image",
            "created_at",
            "updated_at",
        ]

    author_info = ProfileSerializer(source="author.profile", read_only=True)
    tags = TagListField(required=False)
    estimated_reading_time = serializers.ReadOnlyField()
    banner_image = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    claps_count = serializers.ReadOnlyField()
    responses = ResponseSerializer(many=True, read_only=True)
    responses_count = serializers.IntegerField(source="responses.count", read_only=True)
    bookmarks = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_responses_count(self, obj):
        return obj.responses.count()

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_clap_count(self, obj):
        return obj.claps_count()

    def get_banner_image(self, obj):
        return obj.banner_image.url

    def get_views(self, obj):
        return ArticleView.objects.filter(article=obj).count()

    def get_bookmarks(self, obj):
        return Bookmark.objects.filter(article=obj).count()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%B %d, %Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%B %d, %Y")

    # `create` has to be overridden because `estimated_reading_time` is a read-only field.
    def create(self, validated_data):
        tags = validated_data.pop("tags")
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article

    # `update` has to be overridden because `estimated_reading_time` is a read-only field.
    def update(self, instance, validated_data):
        instance.author = validated_data.get("author", instance.author)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.body = validated_data.get("body", instance.body)
        instance.banner_image = validated_data.get(
            "banner_image", instance.banner_image
        )
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)

        if "tags" in validated_data:
            instance.tags.set(validated_data["tags"])

        instance.save()

        return instance


class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
        fields = ["id", "article_title", "user_first_name", "user_last_name"]

    article_title = serializers.CharField(source="article.title", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)

    def get_claps(self, obj):
        return obj.claps.count()
