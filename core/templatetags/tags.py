from django import template

register = template.Library()
@register.filter(name='price')
def cut(value):
    value = round(value, 2)
    return str(value).replace('.', ',')