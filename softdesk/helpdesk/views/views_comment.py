from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from ..models import Comment, Issue
from ..serializers.serializers_comment import CommentSerializer
from ..permissions import IsAuthor, IsContributor


class CommentViewSet(ModelViewSet):
    """
    API endpoints to create, view or edit a comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        # issues_pk is the primary key of issue
        print(self.kwargs.get)
        return Comment.objects.filter(issue=self.kwargs.get('issue_pk'))

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, IsContributor]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(
            issue=Issue.objects.get(pk=self.kwargs.get('issue_pk')),
            author=self.request.user
            )
