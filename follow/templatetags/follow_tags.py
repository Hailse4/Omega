from django import template 

register = template.Library()

@register.filter
def inc_count(value):
    value += 1
    return value 