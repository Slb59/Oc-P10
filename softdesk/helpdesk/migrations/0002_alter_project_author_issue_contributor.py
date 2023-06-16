# Generated by Django 4.2.2 on 2023-06-16 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("helpdesk", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author_project",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Issue",
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
                ("title", models.CharField(max_length=128)),
                ("description", models.CharField(blank=True, max_length=512)),
                (
                    "tag",
                    models.CharField(
                        choices=[("BUG", "Bug"), ("TSK", "Task"), ("UPG", "Upgrade")],
                        default="BUG",
                        max_length=3,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[("LOW", "Low"), ("MED", "Medium"), ("HIG", "High")],
                        default="LOW",
                        max_length=3,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PND", "Pending"), ("OPN", "Open"), ("CLO", "Close")],
                        default="PND",
                        max_length=7,
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author_issue",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helpdesk.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contributor",
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
                    "permission",
                    models.CharField(
                        choices=[("RD", "Read"), ("UD", "Update and delete")],
                        default="UD",
                        max_length=2,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("AUTH", "Author"),
                            ("MANG", "Manager"),
                            ("CREA", "Creator"),
                        ],
                        default="AUTH",
                        max_length=4,
                    ),
                ),
                (
                    "project_contributor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_contributor",
                        to="helpdesk.project",
                    ),
                ),
                (
                    "user_contributor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_contributor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
