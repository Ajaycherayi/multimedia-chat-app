import traceback
from django import template
register = template.Library()
from django.core.cache import cache

@register.simple_tag()
def get_sender_name(user_data, sender_id):
    sender = user_data.get(sender_id, {})
    return sender['name'] if sender['name'] else 'Anonymous'

@register.simple_tag()
def get_sender_profile(user_data, sender_id):
    sender = user_data.get(sender_id, {})
    return sender['profile_image'] if sender['profile_image'] else 'Anonymous'