# Generated by Django 4.1.6 on 2023-02-05 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0004_alter_author_options_alter_book_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Compare",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comparing_books",
                        to="catalog.book",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]