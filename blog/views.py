from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import ListView, FormView, DetailView, CreateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import Post, Subscription, subscribe, unsubscribe, mark_viewed, mark_unviewed


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


class FollowsListView(LoginRequiredMixin, ListView):

    model = User
    template_name = 'blog/follow_user_list.html'

    def get_queryset(self):
        try:
            subscription = self.request.user.subscription
        except Subscription.DoesNotExist:
            return self.model.objects.none()

        return subscription.follows_to.all()


class SubscribeView(LoginRequiredMixin, RedirectView):

    pattern_name = 'users'

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        subscribe(self.request.user, user)
        return super(SubscribeView, self).get_redirect_url()


class UnsubscribeView(LoginRequiredMixin, RedirectView):

    pattern_name = 'follows'

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        unsubscribe(self.request.user, user)
        mark_unviewed(self.request.user, user.post_set.all())
        return super(UnsubscribeView, self).get_redirect_url()


class UserListView(ListView):

    model = User
    template_name = 'blog/user_list.html'

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_active=True).exclude(username=self.request.user)


class CreatePostView(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['header', 'text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)


class PostView(DetailView):

    model = Post


class PostMarkViewedView(LoginRequiredMixin, RedirectView):

    pattern_name = 'post'
    get_viewed = True

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if self.get_viewed:
            mark_viewed(self.request.user, post)
        else:
            mark_unviewed(self.request.user, post)
        self.url = self.request.META.get('HTTP_REFERER')
        return super(PostMarkViewedView, self).get_redirect_url(*args, **kwargs)


class DeletePostView(LoginRequiredMixin, DeleteView):

    model = Post
    success_url = reverse_lazy('posts')

    def is_owner(self):
        post = self.get_object()
        return self.request.user == post.user

    def get(self, request, *args, **kwargs):
        if not self.is_owner():
            return HttpResponseForbidden('у вас нет прав на удаление этого поста')
        return super(DeletePostView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not self.is_owner():
            return HttpResponseForbidden('у вас нет прав на удаление этого поста')
        return super(DeletePostView, self).delete(request, *args, **kwargs)


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


def testview(request, *args, **kwargs):
    return HttpResponse('test view !')
