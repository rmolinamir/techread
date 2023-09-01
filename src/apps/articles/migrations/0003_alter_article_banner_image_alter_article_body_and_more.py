# Generated by Django 4.1.7 on 2023-09-01 02:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0002_article_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="banner_image",
            field=models.ImageField(
                null=True, upload_to="", verbose_name="Banner Image"
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="body",
            field=models.TextField(blank=True, verbose_name="Article Content"),
        ),
        migrations.AlterField(
            model_name="article",
            name="description",
            field=models.TextField(blank=True, verbose_name="Article Description"),
        ),
    ]