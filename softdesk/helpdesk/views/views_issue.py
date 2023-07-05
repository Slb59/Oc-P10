from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from ..models import Project, Issue
from ..serializers.serializers_issue import IssueSerializer
from ..permissions import IsAuthor, IsContributor


class IssueViewSet(ModelViewSet):
    """
    API endpoints to create, view or edit an issue
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self, *args, **kwargs):
        # projects_pk is the primary key of project
        print(self.kwargs.get)
        return Issue.objects.filter(project=self.kwargs.get('projects_pk'))

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(
            project=Project.objects.get(pk=self.kwargs.get('projects_pk')))

    def perform_update(self, serializer, *args, **kwargs):
        serializer.save(
            project=Project.objects.get(pk=self.kwargs.get('projects_pk')))

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated, IsContributor]
        return [permission() for permission in permission_classes]
