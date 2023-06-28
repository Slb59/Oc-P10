from rest_framework.viewsets import ModelViewSet

from .models import Project, Issue
from .serializers_issue import IssueSerializer


class IssueViewSet(ModelViewSet):
    """
    API endpoints to create, view or edit an issue
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self, *args, **kwargs):
        # project_pk is the primary key of project
        return Issue.objects.filter(project=self.kwargs.get('project_pk'))

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(
            project=Project.objects.get(pk=self.kwargs.get('project_pk')))

    def perform_update(self, serializer, *args, **kwargs):
        serializer.save(
            project=Project.objects.get(pk=self.kwargs.get('project_pk')))
