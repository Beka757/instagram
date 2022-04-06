from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from accounts.models import Profile


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=50, label='Имя пользователя', required=True)
    password = forms.CharField(
        label='Пароль', strip=False, required=True, widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label='Подтвердите пароль', strip=False, required=True, widget=forms.PasswordInput
    )
    email = forms.EmailField(label='Почта', required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают!')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'first_name', 'password', 'password_confirm', 'email'
        ]


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class UserChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'subscriptions', 'likes']


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(strip=False, widget=forms.PasswordInput)
    password_old = forms.CharField(strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_password_old(self):
        password_old = self.cleaned_data.get('password_old')
        if not self.instance.check_password(password_old):
            raise forms.ValidationError('Не правильно указан старый пароль!')
        return password_old

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data['password_confirm'])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'password_old']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)


class FollowForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['subscriptions', 'user', 'avatar']
