from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .models import Comment
from .serializers_comment import CommentSerializer
from .permissions import IsAuthor, IsContributor


class CommentViewSet(ModelViewSet):
    """
    API endpoints to create, view or edit a comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        # issues_pk is the primary key of issue
        print(self.kwargs.get)
        return Comment.objects.filter(issue=self.kwargs.get('issues_pk'))

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, IsContributor]
        return [permission() for permission in permission_classes]
