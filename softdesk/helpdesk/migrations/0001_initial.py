# Generated by Django 4.2.2 on 2023-06-19 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("project_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=128)),
                ("description", models.CharField(default="", max_length=512)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("BKE", "Backend"),
                            ("FRE", "Frontend"),
                            ("AND", "Android"),
                            ("IOS", "Ios"),
                        ],
                        default="BKE",
                        max_length=3,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author_project",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                ("issue_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=128)),
                ("description", models.CharField(default="", max_length=512)),
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
                ("contributor_id", models.AutoField(primary_key=True, serialize=False)),
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
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("description", models.CharField(default="", max_length=512)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author_comment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "issue",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issue",
                        to="helpdesk.issue",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="project",
            constraint=models.UniqueConstraint(
                fields=("title",), name="unique_project"
            ),
        ),
    ]
