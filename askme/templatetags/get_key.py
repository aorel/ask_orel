from django import template

register = template.Library()


@register.filter
def get_key(d, k):
    return d[k]
