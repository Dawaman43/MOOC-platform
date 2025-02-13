from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value of a dictionary by key."""
    return dictionary.get(key)
