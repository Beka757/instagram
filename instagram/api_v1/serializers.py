from rest_framework import serializers
from webapp.models import Posts


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['id', 'text', 'user', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']
