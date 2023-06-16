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
