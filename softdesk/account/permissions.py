from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """ Describe the access permission for user endpoints """

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update',
                             'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj == request.user or request.user.is_superuser
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_superuser
        elif view.action == 'destroy':
            return request.user.is_superuser
        else:
            return False
