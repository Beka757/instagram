from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from accounts.forms import (
    UserCreationForm, ProfileCreationForm, UserChangeForm,
    ProfileChangeForm, PasswordChangeForm, SearchForm,
    FollowForm
)
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import DetailView, UpdateView, ListView

from accounts.models import Profile
from webapp.helpers import SearchView
from webapp.models import Posts


class HomePageView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'profile/home_page.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Posts.objects.filter(user_id__in=self.request.user.profile.subscriptions.all()).order_by(
            '-created_at')
        return context


class LoginView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'next': request.GET.get('next')
        }
        return render(request, 'registration/login.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_page = request.GET.get('next')
        if user is not None:
            login(request, user)
            if next_page:
                return redirect(next_page)
            return redirect('home_page')
        else:
            context['has_error'] = True
        return render(request, 'registration/login.html', context=context)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect('home_page')


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        profile_form = ProfileCreationForm()
        genders = Profile.GENDER_CHOICES
        return render(request, 'registration/register.html', context={
            'form': form,
            'genders': genders,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(data=request.POST)
        profile_form = ProfileCreationForm(request.POST, request.FILES)
        next_page = request.GET.get('next')
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            login(request, user)
            if next_page is not None:
                return redirect(next_page)
            return redirect('home_page',)
        return render(request, 'registration/register.html', context={
            'form': form,
            'genders': Profile.GENDER_CHOICES,
            'profile_form': profile_form
        })


class DetailUserView(DetailView):
    model = get_user_model()
    template_name = 'profile/detail_user.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.user_post.order_by('-created_at')
        context['user'] = self.kwargs.get('pk')
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'profile/user_profile_change.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
            kwargs['genders'] = Profile.GENDER_CHOICES
        return super().get_context_data(**kwargs)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(
            form=form, profile_form=profile_form,
            genders=Profile.GENDER_CHOICES
        )
        return self.render_to_response(context)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def get_success_url(self):
        return reverse('detail_user_view', kwargs={'pk': self.object.pk})


class ChangePasswordView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'profile/change_password.html'
    form_class = PasswordChangeForm

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)

    def get_success_url(self):
        return reverse('login_view')


class SearchProfileView(SearchView):
    template_name = 'profile/search_users.html'
    model = get_user_model()
    context_object_name = 'profiles'
    search_form = SearchForm
    search_fields = {
        'username': 'icontains',
        'first_name': 'icontains',
        'email': 'icontains'
    }


class FollowingView(UpdateView):
    model = get_user_model()
    form_class = FollowForm
    template_name = 'profile/detail_user.html'
    context_object_name = 'user_obj'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            profile = self.kwargs.get('pk')
            request_user = self.request.user
            request_user.profile.subscriptions.add(profile)
            url = reverse('detail_user_view', kwargs={
                'pk': profile
            })
            return HttpResponseRedirect(url)
        return render(request, self.template_name, context={'form': form})
