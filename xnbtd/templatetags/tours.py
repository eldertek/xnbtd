from datetime import timedelta

from django import template
from django.db.models import Sum


register = template.Library()

@register.simple_tag
def calculate_total(queryset, column):
    """
    Calculate the total for a given column in a queryset

    Arguments:
        queryset (QuerySet): The queryset that is being used to calculate the total.
        column (str): The column for which the total is being calculated.

    Returns:
        float: The total of the column
    """
    if queryset.exists():
        model_class = queryset.model
        field_type = model_class._meta.get_field(column).get_internal_type()
        if field_type == 'IntegerField' or field_type == 'FloatField':
            total = queryset.aggregate(total=Sum(column)).get('total')
            return total
        elif field_type == 'TimeField':
            total_time = timedelta()
            for item in queryset:
                value = getattr(item, column)
                if value:                    
                    total_time += timedelta(hours=value.hour, minutes=value.minute, seconds=value.second)

            # Calculate total hours and return
            total_hours = total_time.total_seconds() / 3600
            return total_hours

    return None
