from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from webapp.forms import PostForm
from webapp.models import Posts, Like


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


class LikePost(LoginRequiredMixin, CreateView):
    model = Like

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')})

    def post(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        post = get_object_or_404(Posts, pk=post_pk)
        Like.objects.get_or_create(
            user=self.request.user,
            publication=post
        )
        return redirect(self.get_success_url())
