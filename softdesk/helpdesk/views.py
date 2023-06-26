from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer


class ProjectViewSet(ModelViewSet):
    """
    API endpoints to create, view, edit or delete a project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributors=self.request.user)


class ContributorViewSet(ModelViewSet):
    """
    API endpoints to create, view or edit a contributor
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        # project_pk is the primary key of project
        return Contributor.objects.filter(
            project_contributor=self.kwargs.get('project_pk'))

    def perform_create(self, serializer, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs.get('project_pk'))

        # Check if the user is is already contributor
        user_list = [
            user.user_id.id for user in Contributor.objects.filter(
                project_contributor=project)
            ]
        if self.request.data.get('user_id') in user_list:
            raise ValidationError("this user is already contributor")
        else:
            serializer.save(project_id=project)
