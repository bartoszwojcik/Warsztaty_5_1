from django import template

register = template.Library()


@register.filter(name="filter_comments")
def filter_comments(objects):
    return objects.filter(blocked=False)
