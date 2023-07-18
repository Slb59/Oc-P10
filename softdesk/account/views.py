from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .models import User
from .serializers import UserSerializer, UserSignupSerializer
from .permissions import UserPermission


class UserViewSet(ModelViewSet):

    """
    User management.
    Groups all access points for creating, updating and deleting users.
    A user must be 15 years old to register
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    detail_serializer_class = UserSignupSerializer
    permission_classes = [UserPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def options(self, request, *args, **kwargs):
        """
        Don't include the view description in OPTIONS responses.
        """
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data.pop('description')
        return Response(data=data, status=status.HTTP_200_OK)
