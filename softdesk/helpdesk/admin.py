from django.contrib import admin

from .models import Project, Issue, Comment
from .models import Contributor


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "type"]
    list_filter = ["type"]
    search_fields = ["title", "description"]
    raw_id_fields = ["contributors"]


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["title", "tag", "priority", "status", "created_time"]
    list_filter = ["tag", "priority", "status"]
    search_fields = ["title", "description"]
    ordering = ["created_time"]
    raw_id_fields = ["author", "assignee"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["description", "created_time", "issue", "author"]
    search_fields = ["description", "author__username"]
    ordering = ["created_time"]
    raw_id_fields = ["author"]


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = [
        "project_contributor", "user_contributor", "role"
        ]
    list_filter = ["role"]
    search_fields = [
        "project_contributor__title", "user_contributor__username"
        ]
    ordering = ["project_contributor"]
    raw_id_fields = ["project_contributor", "user_contributor"]
