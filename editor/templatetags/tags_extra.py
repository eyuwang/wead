"""
Extra template tags
"""
import ast
import bleach

from django import template
from editor.models import Users

register = template.Library()

@register.simple_tag
def render_date(*args, **kwargs):
    html = "<small>%s</small>" % args[0].strftime('%Y-%m-%d %H:%M:%S')
    return html

@register.simple_tag
def render_author(*args, **kwargs):
    if isinstance(args[0], Users):
        html = "<small>%s %s</small>" % (args[0].first_name.title(), args[0].last_name.title())
    else:
        html = "<small>%s</small>" % args[0].title()
    return html
