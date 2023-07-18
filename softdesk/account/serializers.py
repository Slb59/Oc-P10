from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        self.birth_date_check()
        user = User.objects.create_user(**validated_data)
        return user
    
    def birth_date_check(self):
        # Ensures constraint on model level, raises ValidationError
        if self.age < 15:
            # raise error for field
            raise ValidationError(
                {'birth_date': _('The user must be at least 15 years old')}
                )
