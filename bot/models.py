from django.db import models


class MessageLike(models.Model):
    message_id = models.IntegerField(unique=True)
    data = models.JSONField(default=dict)
