from django.contrib import admin
from messaging.models import Tweet


@admin.register(Tweet)
class Tweet(admin.ModelAdmin):
    pass
