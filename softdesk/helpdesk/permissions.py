from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    # Custom permission for project author
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False
