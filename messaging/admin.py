from django.contrib import admin
from messaging.models import Tweet, PrivateMessage


@admin.register(Tweet)
class Tweet(admin.ModelAdmin):
    pass


@admin.register(PrivateMessage)
class PrivateMessage(admin.ModelAdmin):
    pass
