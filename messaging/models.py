from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    content = models.CharField(max_length=140)
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default="Removed"
    )

    def __str__(self):
        return str(self.id)

    @property
    def content_short(self):
        if len(self.content) > 30:
            return self.content[:30] + "..."
        else:
            return self.content

    @property
    def comment_count(self):
        return Comment.objects.filter(tweet=self).count()


class Comment(models.Model):
    content = models.CharField(max_length=60)
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default="Removed"
    )

    @property
    def content_short(self):
        if len(self.content) > 30:
            return self.content[:30] + "..."
        else:
            return self.content


class PrivateMessage(models.Model):
    content = models.TextField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default="Removed",
        related_name="message_sender"
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default="Removed",
        related_name="message_recipient"
    )
    read_status = models.BooleanField()     # True for read, False for unread

    @property
    def content_short(self):
        if len(self.content) > 30:
            return self.content[:30] + "..."
        else:
            return self.content
