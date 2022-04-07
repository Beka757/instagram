from rest_framework import serializers
from webapp.models import Posts, Like


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['id', 'text', 'user', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id', 'user', 'publication']
