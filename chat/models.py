from django.db import models
from uuid import uuid4
from django.forms import ValidationError
from core.models import User
from django.conf import settings
# Create your models here.


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    CHAT_TYPES = [
        ('group', 'Group Chat'),
        ('private', 'Private Chat'),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)
    chat_type = models.CharField(max_length=20, choices=CHAT_TYPES)

    members = models.ManyToManyField('core.User', related_name='chat_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.chat_type == 'private' and self.members.count() > 2:
            raise ValidationError("Private chat can't have more than 2 members")



class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    group = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        'core.User',
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    content = models.TextField()
    is_edited = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']