# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
# from rest_framework import generics
# from rest_framework.decorators import api_view
from rest_framework import status
# from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema


from .models import User
from .serializers import UserSerializer, UserSignupSerializer
from .permissions import UserPermission


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    detail_serializer_class = UserSignupSerializer
    permission_classes = [UserPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViewSet2(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserAuthenticatedViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Liste des utilisateurs"
        + " enregistrés dans le système",
        responses={200: UserSerializer}
    )
    # @login_required
    # @action(
    #     methods=['get'],
    #     detail=True,
    #     permission_classes=[permissions.IsAuthenticated],
    #     url_path='list', url_name='list')
    def list(self, request):
        queryset = self.get_queryset()
        # permission_classes = [permissions.IsAuthenticated]
        # permission = permissions.IsAuthenticated
        serializer = UserSignupSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.data
        serializer = UserSignupSerializer(data=user)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )

        return Response(
             {"Errors": serializer.errors},
             status=status.HTTP_400_BAD_REQUEST
            )
