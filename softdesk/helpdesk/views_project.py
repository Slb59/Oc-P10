from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Project, Contributor, User
from .serializers_project import ProjectSerializer, ProjectDetailSerializer
from .serializers_project import ContributorSerializer
from .permissions import IsAuthor, IsContributor, IsAuthorContributor
from .permissions import NoPermission


response_project_schema_200 = {
    "200": openapi.Response(
        description="200 description",
        examples={
            "application/json": {
                "200_id": "project_id",
                "200_title": "Project title",
                "200_description": "Description of the project",
                "200_type": "BKE for backend for example",
                "200_contributors": "Liste of contributors",
                "200_author": "user that create the project",
            }
        }
    ),
}
response_project_schema_201 = {
    "201": openapi.Response(
        description="200 description",
        examples={
            "application/json": {
                "200_id": "a new project_id",
                "200_title": "Project title",
                "200_description": "Description of the project",
                "200_type": "BKE for backend for example",
                "200_contributors": "the user as author",
            }
        }
    ),
}


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="List only the project if "
    + "the connected user is a contributor",
    responses=response_project_schema_200
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Any connected user can create a projet"
    + "he would be the author",
    responses=response_project_schema_201
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="User must be a contributor to read the project",
    responses=response_project_schema_200
))
class ProjectViewSet(ModelViewSet):
    """
    User must be the author for update or delete the project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        else:
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
        # projects_pk is the primary key of project
        return Contributor.objects.filter(
            project_contributor=self.kwargs.get('projects_pk'))

    def perform_create(self, serializer, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs.get('projects_pk'))

        # Check if the user is already contributor
        user_list = [
            user.user_contributor.id for user in Contributor.objects.filter(
                project_contributor=project)
            ]
        if self.request.data.get('user_contributor') in user_list:
            raise ValidationError("this user is already contributor")
        else:
            if self.request.data.get('role') == 'AUTH':
                if project.author is None:
                    project_author = User.objects.get(
                        pk=self.request.data.get('user_contributor'))
                    project.author = project_author
                    project.save()
                else:
                    # it's impossible to have two authors
                    raise IntegrityError
            serializer.save(project_contributor=project)

    def perform_destroy(self, instance):

        if instance.role == 'AUTH':
            project = Project.objects.get(pk=self.kwargs.get('projects_pk'))
            project.author = None
            project.save()

        return super().perform_destroy(instance)

    def get_permissions(self):
        if self.action in ['destroy', 'create']:
            permission_classes = [
                permissions.IsAuthenticated,
                IsAuthorContributor
                ]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [
                NoPermission,
            ]
        else:
            permission_classes = [permissions.IsAuthenticated, IsContributor]
        return [permission() for permission in permission_classes]
