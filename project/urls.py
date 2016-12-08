"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from blog.views import LentaView, LoginView, logout_view, testview, UserListView, PostListView, \
    MyPostListView, CreatePostView, PostView, DeletePostView, FollowsListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^$', LentaView.as_view(), name='lenta'),  # lenta of a logined user
    url(r'^users/$', UserListView.as_view(), name='users'),  # all users
    url(r'^users/(?P<username>[\w.@+-]+)/posts/$', PostListView.as_view(), name='user'),  # all posts of the user
    url(r'^posts/$', MyPostListView.as_view(), name='posts'),  # all posts of a logined user
    url(r'^posts/(?P<pk>[0-9]+)/$', PostView.as_view(), name='post'),  # the post
    url(r'^posts/add/$', CreatePostView.as_view(), name='create_post'),
    url(r'^posts/(?P<pk>[0-9]+)/delete$', DeletePostView.as_view(), name='delete_post'),
    url(r'^follows/$', FollowsListView.as_view(), name='follows'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
