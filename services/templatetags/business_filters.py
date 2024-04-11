from django import template
import logging

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)

