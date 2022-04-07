from rest_framework import serializers
from webapp.models import Posts, Like, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['id', 'text', 'user', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id', 'user', 'publication']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'post', 'date_publication']
        read_only_fields = ['id', 'date_publication']
