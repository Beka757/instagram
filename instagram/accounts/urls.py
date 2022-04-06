from django.urls import path

from accounts.views import (
    LoginView, LogoutView, RegisterView, DetailUserView,
    UserProfileUpdateView, ChangePasswordView, SearchProfileView,
    FollowingView
)

urlpatterns = []

accounts_urls = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('profile/<int:pk>', DetailUserView.as_view(), name='detail_user_view'),
    path('profile/update', UserProfileUpdateView.as_view(), name='update_profile'),
    path('profile/change_password', ChangePasswordView.as_view(), name='change_password'),
    path('profile/search', SearchProfileView.as_view(), name='search_profile'),
    path('profile/<int:pk>/following', FollowingView.as_view(), name='following')
]

urlpatterns += accounts_urls
