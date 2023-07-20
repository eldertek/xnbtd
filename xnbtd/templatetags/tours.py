from django import template
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def calculate_total(queryset, column):
    total = queryset.aggregate(total=Sum(column)).get('total')
    return total
