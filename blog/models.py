from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, verbose_name='автор')
    header = models.CharField('заголовок', max_length=128)
    text = models.TextField('текст')
    date = models.DateTimeField('дата публикации', default=timezone.now)

    def __str__(self):
        return self.header


class Subscription(models.Model):
    subscriber = models.OneToOneField(User, verbose_name='подписчик')
    follows_to = models.ManyToManyField(User, verbose_name='блоги', related_name='followers')

    def __str__(self):
        return self.subscriber.get_username()

    def get_follows_to(self):
        return ', '.join(list(self.follows_to.values_list('username', flat=True)))


class Viewed(models.Model):
    user = models.OneToOneField(User)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.user.get_username()

    def get_viewed_posts_id(self):
        return ', '.join(list(map(lambda i: str(i), self.posts.values_list('id', flat=True))))


def subscribe(subscriber, users):
    """
    Subscribe `subscriber` on `users` blogs
    :param subscriber: instance of User
    :param users: queryset (list) of instances of User OR instance of User
    """
    obj = Subscription.objects.create(subscriber=subscriber)
    if isinstance(users, (models.QuerySet, list)):
        obj.follows_to.add(*users)
    if isinstance(users, User):
        obj.follows_to.add(users)


def unsubscribe(subscriber, users):
    """
    Unsubscribe `subscriber` from `users` blogs
    :param subscriber: instance of User
    :param users: queryset (list) of instances of User OR instance of User
    """
    obj = Subscription.objects.get(subscriber=subscriber)
    if isinstance(users, (models.QuerySet, list)):
        obj.follows_to.remove(*users)
    if isinstance(users, User):
        obj.follows_to.remove(users)


## operations:

# create_post(user, header, text)

# subscribe(subscriber, to_user)

# unsubscribe(subscriber, from_user)

# mark_viewed(user, post)
