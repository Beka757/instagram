
from django.views.generic import CreateView
from django.urls import reverse
from webapp.forms import CommentForm
from webapp.models import Comment, Posts
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'posts/detail_post.html'
    form_class = CommentForm
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        user = self.request.user.id
        post = get_object_or_404(Posts, pk=post_pk)
        form = self.form_class()
        return render(request, self.template_name, context={'form': form, 'post': post, 'users': user})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = self.request.user.id
            post = self.kwargs.get('pk')
            comment = Comment.objects.create(
                text=form.cleaned_data.get('text'),
                user_id=user
            )
            comment.post.add(post)
            url = reverse('post_detail', kwargs={
                'pk': self.kwargs.get('pk')
            })
            return HttpResponseRedirect(url)
        return render(request, template_name='posts/detail_post.html', context={
            'form': form,
            'post': get_object_or_404(Posts, pk=kwargs.get('pk')),
            'users': self.request.user.id
        })
