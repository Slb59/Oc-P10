from rest_framework import serializers
from softdesk.helpdesk.models import Project, Issue


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

    @staticmethod
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
