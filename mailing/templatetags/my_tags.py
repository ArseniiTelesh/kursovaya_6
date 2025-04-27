from django import template

register = template.Library()


@register.filter
def images_tag(value):
    if value:
        return f'/media/{value}'
    return '#'

@register.simple_tag
def images_tag(value):
    if value:
        return f'/media/{value}'
    return '#'