from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .models import Comment


class CommentViewSet(ModelViewSet):
    """
    API endpoints to create, view or edit a comment
    """
    queryset = Comment.objects.all()