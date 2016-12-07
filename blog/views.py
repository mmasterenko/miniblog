from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import Post, Subscription, Viewed


class LentaView(LoginRequiredMixin, ListView):

    model = Post
    template_name = 'blog/lenta.html'

    def get_queryset(self):
        try:
            subscription = self.request.user.subscription
        except Subscription.DoesNotExist:
            return self.model.objects.none()

        users_follows_to = subscription.follows_to.all()

        return self.model.objects.filter(user__in=users_follows_to)


class UserListView(ListView):

    model = User
    template_name = 'blog/user_list.html'

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_active=True).exclude(username=self.request.user)


class PostListView(ListView):

    model = Post

    def get_queryset(self):
        return Post.objects.filter(user__username=self.kwargs.get('username'))


class MyPostListView(LoginRequiredMixin, PostListView):

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user.id)


class LoginView(FormView):

    form_class = AuthenticationForm
    template_name = 'admin/login.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['site_title'] = 'Авторизация'
        context['site_header'] = 'Введите логин и пароль'
        return context

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super(LoginView, self).form_valid(form)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(redirect_to='/')


def testview(request):
    return HttpResponse('test view !')
