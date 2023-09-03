from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from src.apps.articles.models import Article


@registry.register_document
class ArticleDocument(Document):
    class Index:
        name = "articles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Article
        fields = ["created_at"]

    title = fields.TextField(attr="title")
    description = fields.TextField(attr="description")
    body = fields.TextField(attr="body")
    author_first_name = fields.TextField()
    author_last_name = fields.TextField()
    tags = fields.KeywordField()

    def prepare_author_first_name(self, instance):
        return instance.author.first_name

    def prepare_author_last_name(self, instance):
        return instance.author.last_name

    def prepare_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]
