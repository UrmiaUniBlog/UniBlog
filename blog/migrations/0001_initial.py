# Generated by Django 5.0.1 on 2024-01-13 21:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="IPAddress",
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
                ("ip_address", models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name="Message",
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
                    "name",
                    models.CharField(
                        blank=True, editable=False, max_length=100, null=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, editable=False, max_length=254, null=True
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        blank=True, editable=False, max_length=100, null=True
                    ),
                ),
                ("message", models.TextField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("status", models.BooleanField(default=True)),
                ("position", models.IntegerField()),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="blog.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ["parent__id", "position"],
            },
        ),
        migrations.CreateModel(
            name="Article",
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
                ("title", models.CharField(max_length=200)),
                ("subtitle", models.CharField(blank=True, default="", max_length=200)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.TextField()),
                ("thumbnail", models.ImageField(upload_to="images")),
                ("publish", models.DateTimeField(default=django.utils.timezone.now)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "is_special",
                    models.BooleanField(default=False, verbose_name="Special status"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("d", "Draft"),
                            ("p", "Publish"),
                            ("r", "Reviewing"),
                            ("b", "Denied"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(related_name="articles", to="blog.category"),
                ),
            ],
            options={
                "ordering": ["-publish"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("p", "Publish"),
                            ("r", "Reviewing"),
                            ("b", "Denied(Delete comment)"),
                        ],
                        default="r",
                        max_length=1,
                    ),
                ),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="blog.article",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="blog.comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-article"],
            },
        ),
        migrations.CreateModel(
            name="ArticleHit",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.article"
                    ),
                ),
                (
                    "ip_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.ipaddress"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="hits",
            field=models.ManyToManyField(
                blank=True,
                related_name="hits",
                through="blog.ArticleHit",
                to="blog.ipaddress",
            ),
        ),
    ]
