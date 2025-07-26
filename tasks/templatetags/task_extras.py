from django import template
import datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def duration(td):
    """Format a timedelta as H:MM:SS or M:SS."""
    if not isinstance(td, datetime.timedelta):
        return td
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"