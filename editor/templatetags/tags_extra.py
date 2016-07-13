"""
Extra template tags
"""
import ast
import bleach

from django import template
from editor.models import Users
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_date(*args, **kwargs):
    html = "<small>%s</small>" % args[0].strftime('%Y-%m-%d %H:%M:%S')
    return mark_safe(html)

@register.simple_tag
def render_author(*args, **kwargs):
    if isinstance(args[0], Users):
        html = "<small>%s %s</small>" % (args[0].first_name.title(), args[0].last_name.title())
    else:
        html = "<small>%s</small>" % args[0].title()
    return mark_safe(html)
