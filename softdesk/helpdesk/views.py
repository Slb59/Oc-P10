from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    """
    API endpoints to create, view, edit or delete a project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    # return Project.objects.filter(contributors=self.request.user)
