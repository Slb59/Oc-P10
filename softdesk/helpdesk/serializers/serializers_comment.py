from rest_framework import serializers

from softdesk.helpdesk.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue', 'created_time']
        read_only_fields = ['issue', 'author', 'created_time']

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)

        # author is connected user
        comment.author = self.context.get('request').user
        comment.save()
        return comment
