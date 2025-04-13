import csv

from django.http import HttpResponse
from django.utils import timezone


def export_as_csv(modeladmin, request, queryset, fields=None, exclude=None, filename=None):
    """
    Generic function to export a queryset as CSV

    Args:
        modeladmin: The ModelAdmin instance
        request: The current request
        queryset: The queryset to export
        fields: List of field names to include (if None, all fields are included)
        exclude: List of field names to exclude
        filename: Custom filename (if None, model name is used)

    Returns:
        HttpResponse with CSV attachment
    """
    if not filename:
        meta = modeladmin.model._meta
        model_name = meta.verbose_name_plural.lower().replace(' ', '_')
        date_str = timezone.now().strftime('%Y%m%d')
        filename = f"{model_name}_{date_str}"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    # Get fields to export
    if fields is None:
        fields = [field.name for field in modeladmin.model._meta.fields]
        # Add display methods that are in list_display
        for field_name in modeladmin.list_display:
            if (
                field_name not in fields
                and field_name != '__str__'
                and hasattr(modeladmin, field_name)
            ):
                fields.append(field_name)

    if exclude:
        fields = [f for f in fields if f not in exclude]

    writer = csv.writer(response)

    # Write header row with verbose field names
    header = []
    for field in fields:
        if hasattr(modeladmin, field) and hasattr(getattr(modeladmin, field), 'short_description'):
            header.append(getattr(getattr(modeladmin, field), 'short_description'))
        else:
            try:
                header.append(modeladmin.model._meta.get_field(field).verbose_name)
            except Exception:
                header.append(field)

    writer.writerow(header)

    # Write data rows
    for obj in queryset:
        row = []
        for field in fields:
            if hasattr(modeladmin, field) and callable(getattr(modeladmin, field)):
                # Call the display method and strip HTML tags
                value = getattr(modeladmin, field)(obj)
                # If the value is a SafeString (has HTML), convert to plain text
                if hasattr(value, 'strip_tags'):
                    from django.utils.html import strip_tags

                    value = strip_tags(value)
            else:
                value = getattr(obj, field, '')
                if callable(value):
                    value = value()
            row.append(value)
        writer.writerow(row)

    return response


def export_route_as_csv(modeladmin, request, queryset):
    """
    Action to export route data as CSV
    """
    # Exclude some fields that don't make sense in a CSV export
    exclude = ['id', 'comments']

    # Get the model name for the filename
    model_name = modeladmin.model._meta.verbose_name_plural.lower().replace(' ', '_')
    filename = f"{model_name}_export_{timezone.now().strftime('%Y%m%d')}"

    return export_as_csv(modeladmin, request, queryset, exclude=exclude, filename=filename)


export_route_as_csv.short_description = "Exporter en CSV"


def export_single_route_as_csv(modeladmin, request, object_id):
    """
    Export a single route as CSV
    """
    # Get the object
    obj = modeladmin.model.objects.get(pk=object_id)

    # Create a queryset with just this object
    queryset = modeladmin.model.objects.filter(pk=object_id)

    # Get the model name and route name for the filename
    model_name = modeladmin.model._meta.verbose_name.lower().replace(' ', '_')
    route_name = obj.name.replace(' ', '_')
    date_str = obj.date.strftime('%Y%m%d')

    filename = f"{model_name}_{route_name}_{date_str}"

    # Exclude some fields that don't make sense in a CSV export
    exclude = ['id', 'comments']

    return export_as_csv(modeladmin, request, queryset, exclude=exclude, filename=filename)
