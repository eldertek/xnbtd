
from datetime import datetime, timedelta
from django import template
from xnbtd.plannings.models import Event


register = template.Library()


@register.simple_tag
def get_upcoming_events(count):
    yesterday = datetime.now() - timedelta(days=1)
    return Event.objects.filter(date__gt=yesterday)[:count]
