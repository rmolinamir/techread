# Generated by Django 4.1.7 on 2023-08-31 00:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_last_login"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="user_id",
            new_name="id",
        ),
    ]
