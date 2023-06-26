from rest_framework import serializers
from .models import Project, Contributor


# class ContributorSerializer(serializers.HyperlinkedModelSerializer):

#     id = serializers.ReadOnlyField(source='user_contributor.id')
#     name = serializers.ReadOnlyField(source='user_contributor.username')

#     class Meta:
#         model = Contributor
#         fields = [
#             'id', 'name',
#             'permission', 'role'
#             ]

class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = [
            'id', 'user_contributor',
            'permission', 'role'
            ]


class ProjectSerializer(serializers.ModelSerializer):
    # contributors = ContributorSerializer(
    #     source='contributing', read_only=True, many=True)
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors']

    def get_contributors(self, obj):
        # obj is a project instance, return list of dicts
        queryset = Contributor.objects.filter(project_contributor=obj)
        return [ContributorSerializer(c).data for c in queryset]

    def create(self, validated_data):
        try:
            project = Project.objects.create(**validated_data)

            # Get request user
            request_user = self.context.get('request').user

            # Add user to contributor as author
            contributor = Contributor(
                user_contributor=request_user,
                project_contributor=project,
                permission=Contributor.Permission.ALL,
                role=Contributor.Role.AUTHOR
            )

            # save contributor object
            contributor.save()

            return project

        except KeyError:
            raise serializers.ValidationError('Error in creating project')



