from django.contrib import admin

from .models import Project, Issue, Comment
from .models import Contributor


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """ Spécifications for administration of projects """
    list_display = [
        "title", "description", "type",
        "created_time", "updated_time"
        ]
    list_filter = ["type", "created_time", "updated_time"]
    search_fields = ["title", "description"]
    ordering = ["-created_time"]
    raw_id_fields = ["contributors"]


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """ Spécifications for administration of issues """
    list_display = [
        "title", "tag", "priority", "status",
        "created_time", "updated_time"
        ]
    list_filter = ["tag", "priority", "status"]
    search_fields = ["title", "description"]
    ordering = ["created_time"]
    raw_id_fields = ["author", "assignee"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Spécifications for administration of comments """
    list_display = [
        "description",
        "created_time", "updated_time",
        "issue", "author"]
    search_fields = ["description", "author__username"]
    ordering = ["-created_time"]
    raw_id_fields = ["author", "issue"]


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    """ Spécifications for administration of contributors """
    list_display = [
        "project_contributor", "user_contributor", "role",
        "created_time", "updated_time"
        ]
    list_filter = ["role"]
    search_fields = [
        "project_contributor__title", "user_contributor__username",
        "created_time", "updated_time"
        ]
    ordering = ["project_contributor"]
    raw_id_fields = ["project_contributor", "user_contributor"]
