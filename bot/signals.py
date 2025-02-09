from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from blog.models import Quote, Review

from .bot import send_quote, send_review


@receiver(post_save, sender=Quote)
def checker_quote(sender, instance: Quote, created, **kwargs):
    # if created:
    return send_quote(instance)


@receiver(post_save, sender=Review)
def checker_review(sender, instance: Review, created, **kwargs):
    # if created:
    return send_review(instance)
