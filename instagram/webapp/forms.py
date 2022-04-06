from django import forms
from accounts.models import Profile
from webapp.models import Posts, Comment


class PostForm(forms.ModelForm):
    text = forms.CharField(max_length=2000, required=False)
    image = forms.ImageField(required=True)

    class Meta:
        model = Posts
        fields = ['text', 'image']


class PostLikeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['likes']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'post']

