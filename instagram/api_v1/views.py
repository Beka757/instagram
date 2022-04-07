from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet

from webapp.models import Posts, Like
from rest_framework import viewsets, permissions, mixins
from api_v1.serializers import PostSerializer, LikeSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS


class UpdateOrDeletePermission(BasePermission):
    message = 'Редактирование и удаление постов - только свои!'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class PostViewSet(viewsets.ModelViewSet, UpdateOrDeletePermission):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [UpdateOrDeletePermission]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return JsonResponse({'status': 'OK'})


class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]
