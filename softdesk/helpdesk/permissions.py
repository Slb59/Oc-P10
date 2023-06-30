from rest_framework import permissions
from .models import Project


class IsAuthor(permissions.BasePermission):
    # Custom permission for project, issue and comment author
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsAuthorContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        project_pk = view.kwargs.get('projects_pk')
        project = Project.objects.get(pk=project_pk)
        contributors = project.contributors.filter(role='AUTH')
        if request.user in contributors:
            return True
        else:
            return False


class IsContributor(permissions.BasePermission):
    # Custom permission for project contributor
    def has_permission(self, request, view):

        project_pk = view.kwargs.get('projects_pk')
        project = Project.objects.get(pk=project_pk)
        contributors = project.contributors.all()
        if request.user in contributors:
            return True
        else:
            return False
