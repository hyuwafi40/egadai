from django import template

from config.shared.access import user_is_manager

register = template.Library()


@register.filter(name="is_manager")
def is_manager(user):
    return user_is_manager(user)
