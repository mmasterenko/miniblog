from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import Post, Subscription, Viewed


class LentaView(LoginRequiredMixin, ListView):

    model = Post


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
