from django.shortcuts import reverse, render, redirect
from django.views.generic import CreateView, DetailView, UpdateView
from webapp.forms import PostForm, PostLikeForm
from webapp.models import Posts
from django.contrib.auth import get_user_model


class PostDetailView(DetailView):
    template_name = 'posts/detail_post.html'
    model = Posts
    context_object_name = 'post'


class PostCreateView(CreateView):
    template_name = 'posts/create_post.html'
    form_class = PostForm
    model = Posts
    object = None

    def get_success_url(self):
        return reverse('detail_user_view', kwargs={'pk': self.request.user.pk})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            self.object = Posts.objects.create(
                text=form.cleaned_data.get('text'),
                user=self.request.user,
                image=form.cleaned_data.get('image')
            )
            return redirect(self.get_success_url())
        return render(request, self.template_name, context={'form': form})


class PostLikesView(UpdateView):
    template_name = 'posts/detail_post.html'
    form_class = PostLikeForm
    model = get_user_model()

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=self.request.POST)
        if form.is_valid():
            user = self.request.user
            user.profile.likes.add(self.kwargs.get('pk'))
            return redirect(self.get_success_url())
        return render(request, self.template_name, context={'form': form})
