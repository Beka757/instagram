from django.urls import path
from accounts.views import HomePageView
from webapp.views.commen_view import CommentCreateView
from webapp.views.post_views import PostDetailView, PostCreateView, LikePost

urlpatterns = []

profile_urls = [
    path('', HomePageView.as_view(), name='home_page')
]

post_urls = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/like', LikePost.as_view(), name='add_like')
]

comment_urls = [
    path('post/<int:pk>/comment', CommentCreateView.as_view(), name='create_comment')
]

urlpatterns += profile_urls
urlpatterns += post_urls
urlpatterns += comment_urls

