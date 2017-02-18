from django import template

register = template.Library()

@register.filter(name='dict')
def dict(value, arg):
    return value[arg]

@register.filter(name='get_title')
def get_title(value):
    return value.title

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

