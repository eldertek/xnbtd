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
        float or None: The total of the column rounded to two decimal places,
        or None if the total is None.
    """
    # Check if the queryset has been sliced
    try:
        # This will raise an exception if the queryset has been sliced
        exists = queryset.exists()
    except TypeError:
        # The queryset has been sliced, so we need to create a new queryset
        print("DEBUG: Queryset has been sliced in calculate_total, creating a new queryset")
        model = queryset.model
        # Create a new queryset - we can't preserve filters, so we'll use all()
        queryset = model.objects.all()
        exists = queryset.exists()

    if exists:
        model_class = queryset.model
        field_type = model_class._meta.get_field(column).get_internal_type()

        if field_type in ("IntegerField", "FloatField", "DecimalField"):
            total = queryset.aggregate(total=Sum(column)).get("total")
            return round(total, 2) if total is not None else None
        elif field_type == "TimeField":
            total_time = timedelta()

            for item in queryset:
                if value := getattr(item, column):
                    total_time += timedelta(
                        hours=value.hour, minutes=value.minute, seconds=value.second
                    )

            # Calculate total hours and round to 2 decimal places
            total_hours = total_time.total_seconds() / 3600
            return round(total_hours, 2) if total_hours is not None else None

    return None
