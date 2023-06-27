from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema

from .models import Project, Contributor
from .serializers import ProjectSerializer, ProjectDetailSerializer
from .serializers import ContributorSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="List only the project if "
    + "the connected user is a contributor",
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Any connected user can create a projet"
    + "he would be the author",
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="User must be a contributor to read the project",
))
class ProjectViewSet(ModelViewSet):
    """
    User must be the author for update or delete the project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributors=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.detail_serializer_class
        return super().get_serializer_class()


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
