from django import template

register = template.Library()

@register.filter
def times(value):
    l = [i+1 for i in range(value)]
    return l
