from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    class Meta:
        model = User
        fields = [
            'id', 'username',
            'first_name', 'last_name',
            'email', 'post_description', 'is_superuser',
            'birth_date'
            ]


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    class Meta:
        model = User
        fields = [
            'id', 'username',
            'first_name', 'last_name',
            'email', 'password', 'post_description',
            'birth_date'
            ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
