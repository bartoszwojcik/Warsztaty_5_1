from django.contrib import admin
from messaging.models import Tweet, PrivateMessage, Comment


@admin.register(Tweet)
class Tweet(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "creation_date",
        "content_short",
        "comment_count"
    )


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = (
        "id",
        "tweet",
        "author",
        "creation_date"
    )


@admin.register(PrivateMessage)
class PrivateMessage(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "recipient",
        "creation_date",
        "read_status",
        "content_short"
    )
