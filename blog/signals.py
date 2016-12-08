from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from .models import Post


@receiver(post_save, sender=Post, dispatch_uid='notify_followers')
def notify_followers(sender, instance=None, created=None, **kwargs):
    if created:
        recipient_list = []
        for s in instance.user.followers.all():
            recipient_list.append(s.subscriber.email)
        from_email = None  # use DEFAULT_FROM_EMAIL
        subject = 'New Post !'
        message = 'New post "%s" is available !' % instance.header
        send_mail(subject, message, from_email, recipient_list)
