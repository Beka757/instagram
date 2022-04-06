from django.contrib.auth import get_user_model
from django.db import models


class Posts(models.Model):
    text = models.TextField(max_length=2000, null=True, verbose_name='Текст')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_post')
    image = models.ImageField(null=False, blank=True, upload_to='post_pics', verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')


class Comment(models.Model):
    text = models.TextField(max_length=1000, verbose_name='Комментарий')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comment_user', verbose_name='Пользователи')
    post = models.ManyToManyField('webapp.Posts', related_name='comment_post', blank=True, verbose_name='Пост')
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')

