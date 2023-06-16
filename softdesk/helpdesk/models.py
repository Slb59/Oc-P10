from django.db import models
from django.utils.translation import gettext_lazy as _
from softdesk.account.models import User


class Project(models.Model):

    class Platform(models.TextChoices):
        BACKEND = "BKE", _('Backend')
        FRONTEND = "FRE", _('Frontend')
        ANDROID = "AND", _('Android')
        IOS = "IOS", _('Ios')

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True)

    type = models.CharField(
        max_length=3, choices=Platform.choices, default="BKE"
        )
    author = models.ForeignKey(
        to=User, related_name="author",
        on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_project')
        ]

    def __str__(self):
        return "Project:" + self.title

    def get_type(self):
        return Project.Platform(self.type)


class Contributor(models.Model):

    class Permission(models.TextChoices):
        READ = "RD", _('Read')
        ALL = "UD", _('Update and delete')

    class Role(models.TextChoices):
        AUTHOR = "AUTH", _('Author')
        MANAGER = "MANG", _('Manager')
        CREATOR = "CREA", _('Creator')

    user_contributor = models.ForeignKey(
        to=User, related_name="user_contributor", on_delete=models.CASCADE,
        blank=True, null=True
        )

    project_contributor = models.ForeignKey(
        to=Project, related_name="project_contributor",
        on_delete=models.CASCADE,
        blank=True, null=True
        )

    permission = models.CharField(
        max_length=2, choices=Permission.choices, default="UD"
        )

    role = models.CharField(
        max_length=4, choices=Role.choices, default="AUTH")

    def __str__(self):
        return "Contributor:" + str(self.user_id)
