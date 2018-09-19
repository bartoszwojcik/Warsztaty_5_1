from django.contrib import admin
from messaging.models import Tweet, PrivateMessage, Comment


# Admin actions

def block(model_admin, request, query_set):
    query_set.update(blocked=True)


block.short_description = "Block"


def unblock(model_admin, request, query_set):
    query_set.update(blocked=False)


unblock.short_description = "Unblock"


# Admin models

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "creation_date",
        "content_short",
        "blocked",
        "comment_count"
    )

    actions = [block, unblock]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tweet",
        "author",
        "creation_date",
        "content_short",
        "blocked"
    )

    actions = [block, unblock]


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "recipient",
        "creation_date",
        "read_status",
        "content_short",
        "blocked"
    )

    actions = [block, unblock]
