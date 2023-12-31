from django.db import models
from django.utils.translation import gettext_lazy as _

from softdesk.account.models import User


class DateFields(models.Model):
    """ a common class for timestamping """
    created_time = models.DateTimeField(
        auto_now_add=True
    )
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(DateFields):
    """ Spécifications for describing a project """

    class Platform(models.TextChoices):
        BACKEND = "BKE", _('Backend')
        FRONTEND = "FRE", _('Frontend')
        ANDROID = "AND", _('Android')
        IOS = "IOS", _('Ios')

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, default="")

    type = models.CharField(
        max_length=3, choices=Platform.choices, default="BKE"
        )

    author = models.ForeignKey(
        to=User, related_name="author_project",
        on_delete=models.CASCADE, blank=True, null=True)

    contributors = models.ManyToManyField(
        User, through='Contributor', related_name='contributing')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_project')
        ]

    def __str__(self):
        return "Project: " + self.title

    def get_type(self):
        return Project.Platform(self.type)


class Contributor(DateFields):
    """ Spécifications for describing
      a contributor of a project """

    # class Permission(models.TextChoices):
    #     READ = "RD", _('Read')
    #     ALL = "UD", _('Update and delete')

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

    role = models.CharField(
        max_length=4, choices=Role.choices, default="AUTH")

    class Meta:
        unique_together = ('user_contributor', 'project_contributor')

    def __str__(self):
        return "Contributor: " + str(self.user_contributor)


class Issue(DateFields):
    """ Spécifications for describing a issue
     on a project """

    class Tag(models.TextChoices):
        BUG = "BUG", _('Bug')
        TASK = "TSK", _('Task')
        UPGRADE = "UPG", _('Upgrade')

    class Priority(models.TextChoices):
        LOW = "LOW", _('Low')
        MEDIUM = "MED", _('Medium')
        HIGH = "HIG", _('High')

    class Status(models.TextChoices):
        PENDING = "PND", _('Pending')
        OPEN = "OPN", _('Open')
        CLOSED = "CLO", _('Close')

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, default="")
    tag = models.CharField(max_length=3, choices=Tag.choices, default='BUG')
    priority = models.CharField(
        max_length=3, choices=Priority.choices, default="LOW"
        )

    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, blank=True, null=True
        )

    status = models.CharField(
        max_length=7, choices=Status.choices, default="PND"
        )
    author = models.ForeignKey(
        to=User, related_name="author_issue", on_delete=models.CASCADE,
        blank=True, null=True
        )
    assignee = models.ForeignKey(
        to=User, related_name="assignee", on_delete=models.CASCADE,
        blank=True, null=True
        )

    def __str__(self):
        return 'Issue: ' + self.title


class Comment(DateFields):
    """ Spécifications for describing a comment
     on a issue """

    description = models.CharField(max_length=512, default="")
    author = models.ForeignKey(
        to=User, related_name="author_comment", on_delete=models.CASCADE,
        blank=True, null=True
        )
    issue = models.ForeignKey(
        to=Issue, related_name="issue", on_delete=models.CASCADE,
        blank=True, null=True
        )

    def __str__(self):
        return 'Comment: ' + self.description
