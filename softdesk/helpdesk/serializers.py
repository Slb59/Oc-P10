from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Project, Contributor
from .models import Issue


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
        fields = [
            'id', 'title', 'description',
            'type', 'contributors', 'author'
            ]
        extra_kwargs = {
            'type': {
                'help_text': _('can be backend(BKE), '
                               'frontend(FRE), android(AND) or ios(IOS)')},
            'author': {
                'default': serializers.CurrentUserDefault(),
                'help_text': _("The ID of the user that created this project;"
                               "defaults to the currently logged in user.")
            },
        }

    def get_contributors(self, obj):
        # obj is a project instance, return list of dicts
        queryset = Contributor.objects.filter(project_contributor=obj)
        return [ContributorSerializer(c).data for c in queryset]


class ProjectDetailSerializer(serializers.ModelSerializer):
    # contributors = ContributorSerializer(
    #     source='contributing', read_only=True, many=True)

    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description',
            'type', 'contributors'
            ]
        extra_kwargs = {
            'type': {
                'help_text': _('can be backend(BKE), '
                               'frontend(FRE), android(AND) or ios(IOS)')},
        }

    def get_contributors(self, obj):
        # obj is a project instance, return list of dicts
        queryset = Contributor.objects.filter(project_contributor=obj)
        return [ContributorSerializer(c).data for c in queryset]

    def create(self, validated_data):
        """
            create a new project with request_user as author
            and add a contributor link with role author
            between the project and the request_user
        """
        try:
            project = Project.objects.create(**validated_data)

            # Get request user
            request_user = self.context.get('request').user
            project.author = request_user
            project.save()

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


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'project', 'status', 'author',
                  'assignee', 'created_time']
        read_only_fields = ['project', 'author', 'created_time']

    def create(self, validated_data):
        issue = Issue.objects.create(**validated_data)

        # author is connected user
        issue.author = self.context.get('request').user

        issue = self.check_assignee_user(issue)
        issue.save()
        return issue

    def check_assignee_user(issue):
        # Get project
        project = Project.objects.get(pk=issue.project.id)
        project_contributors = project.contributors.all()

        # If assignee is filled, check user is contributors
        # else force to the author as default
        if issue.assignee is not None:
            if issue.assignee not in project_contributors:
                issue.assignee = issue.author

        # If assignee is not filled, set author by default
        else:
            issue.assignee = issue.author
        return issue

    def update(self, instance, validated_data):

        # Get user id
        instance.author = validated_data.get('author', instance.author)
        instance.assignee = validated_data.get('assignee', instance.assignee)

        instance = self.check_assignee_user(instance)
        instance.save()

        return instance
