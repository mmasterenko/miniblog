from django.contrib import admin
from .models import Post, Subscription, Viewed


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'date']
    list_filter = ['user']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_follows_to']


@admin.register(Viewed)
class ViewedAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_viewed_posts_id']
