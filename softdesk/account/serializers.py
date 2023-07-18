from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """ Serialize the User Model for login endpoints """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    class Meta:
        model = User
        fields = [
            'id', 'username',
            'first_name', 'last_name',
            'email', 'post_description', 'is_superuser',
            'birth_date', "can_be_contacted", "can_data_be_shared"
            ]


class UserSignupSerializer(serializers.ModelSerializer):
    """ Serialize the User Model for signup endpoints """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    class Meta:
        model = User
        fields = [
            'id', 'username',
            'first_name', 'last_name',
            'email', 'password', 'post_description',
            'birth_date', "can_be_contacted", "can_data_be_shared"
            ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
