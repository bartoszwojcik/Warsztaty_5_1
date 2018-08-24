from django.contrib import admin
from twitter.models import Tweet


@admin.register(Tweet)
class Tweet(admin.ModelAdmin):
    pass
