from django.urls import include, path
from rest_framework import routers
from api_v1.views import PostViewSet, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'posts', viewset=PostViewSet)
app_name = 'api_v1'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='api_token_auth')
]
