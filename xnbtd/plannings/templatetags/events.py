from datetime import datetime, timedelta

from django import template

from xnbtd.plannings.models import Event


register = template.Library()


@register.simple_tag
def get_upcoming_events_grouped(count):
    yesterday = datetime.now() - timedelta(days=1)
    events = Event.objects.filter(date__gt=yesterday)[:count]

    grouped_events = {}
    for event in events:
        event_date = event.date
        if event_date == datetime.now().date():
            date_key = "Aujourd'hui"
        elif event_date == (datetime.now() + timedelta(days=1)).date():
            date_key = "Demain"
        else:
            date_key = event_date

        if date_key in grouped_events:
            grouped_events[date_key].append(event)
        else:
            grouped_events[date_key] = [event]

    return grouped_events
