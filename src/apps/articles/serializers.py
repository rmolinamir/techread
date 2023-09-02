from rest_framework import serializers
from src.apps.profiles.serializers import ProfileSerializer
from .models import Article, ArticleView


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
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_banner_image(self, obj):
        return obj.banner_image.url

    def get_views(self, obj):
        return ArticleView.objects.filter(article=obj).count()

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
