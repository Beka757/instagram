from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Мужской'),
        ('FEMALE', 'Женский')
    ]
    user = models.OneToOneField(
        get_user_model(), related_name='profile',
        on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    avatar = models.ImageField(upload_to='user_pics', verbose_name='Аватар')
    user_information = models.TextField(max_length=2000, null=True, blank=True,
                                        verbose_name='Информация о пользователе')
    phone_number = PhoneNumberField(unique=True, region='KZ', null=True, blank=True,  verbose_name='Номер телефона')
    gender = models.CharField(max_length=6, null=True, blank=True, choices=GENDER_CHOICES, verbose_name='Пол')
    subscriptions = models.ManyToManyField(
        get_user_model(), related_name='subscribers', verbose_name='Подписки', blank=True
    )
    likes = models.ManyToManyField('webapp.Posts', related_name='profile_like', blank=True)

    def __str__(self):
        return f'{self.user.get_full_name()}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
