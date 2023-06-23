from rest_framework import serializers
from .models import Project, Contributor


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors']

        def create(self, validated_data):
            project = Project.objects.create(**validated_data)

            # Get user id
            request_user = self.context['request'].user

            # Add user to contributor
            Contributor.objects.create(
                user_contributor=request_user,
                project_contributor=project,
                permission=Contributor.Permission.ALL,
                role=Contributor.Role.AUTHOR
                )

            return project
