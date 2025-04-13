from calendar import monthrange
from datetime import datetime

from django import template
from django.db.models import Sum


register = template.Library()


@register.simple_tag
def calculate_gls_delivered_packages_price(queryset):
    """
    Calculate the price for GLS delivered packages based on the pricing tiers:
    - 3.17€ per package for the first 18671 packages per month
    - 2.82€ per package for packages beyond 18671 per month

    Args:
        queryset: A queryset of GLS objects filtered for a specific month

    Returns:
        float: The total price for delivered packages
    """
    if not queryset.exists():
        return 0

    # Get the total number of delivered packages for the month
    total_packages = queryset.aggregate(total=Sum('packages_delivered')).get('total', 0) or 0

    # Calculate price based on tiers
    if total_packages <= 18671:
        return round(total_packages * 3.17, 2)
    else:
        tier1_price = 18671 * 3.17
        tier2_price = (total_packages - 18671) * 2.82
        return round(tier1_price + tier2_price, 2)


@register.simple_tag
def calculate_gls_pickup_packages_price(queryset):
    """
    Calculate the price for GLS pickup packages:
    - 1.52€ per regular pickup package
    - 1.5€ per occasional pickup (EO)

    Args:
        queryset: A queryset of GLS objects

    Returns:
        dict: A dictionary with regular_pickup_price, eo_price, and total_price
    """
    if not queryset.exists():
        return {'regular_pickup_price': 0, 'eo_price': 0, 'total_price': 0}

    # Get the total number of regular pickup packages
    regular_pickup = queryset.aggregate(total=Sum('pickup_point')).get('total', 0) or 0

    # Get the total number of occasional pickups (EO)
    eo_pickup = queryset.aggregate(total=Sum('eo')).get('total', 0) or 0

    # Calculate prices
    regular_pickup_price = round(regular_pickup * 1.52, 2)
    eo_price = round(eo_pickup * 1.5, 2)
    total_price = round(regular_pickup_price + eo_price, 2)

    return {
        'regular_pickup_price': regular_pickup_price,
        'eo_price': eo_price,
        'total_price': total_price,
    }


@register.simple_tag
def calculate_gls_shd_price(queryset):
    """
    Calculate the price for SHD entries:
    - 3.17€ for the first entry of each SHD
    - 0.63€ for the second entry of each SHD
    - 0.32€ for the third and subsequent entries of each SHD

    Args:
        queryset: A queryset of GLS objects

    Returns:
        float: The total price for SHD entries
    """
    if not queryset.exists():
        return 0

    total_price = 0

    # Process each GLS object in the queryset
    for gls in queryset:
        # Get all SHD entries for this GLS object, ordered by number
        shd_entries = gls.shd_entries.all().order_by('number')

        # Calculate price based on position
        for i, entry in enumerate(shd_entries):
            if i == 0:  # First entry
                total_price += 3.17 * entry.value
            elif i == 1:  # Second entry
                total_price += 0.63 * entry.value
            else:  # Third and subsequent entries
                total_price += 0.32 * entry.value

    return round(total_price, 2)


@register.simple_tag
def get_month_gls_queryset(queryset, year, month):
    """
    Filter a GLS queryset to only include entries from a specific month and year

    Args:
        queryset: The original GLS queryset
        year: The year to filter by
        month: The month to filter by (1-12)

    Returns:
        QuerySet: A filtered queryset containing only the specified month's data
    """
    # Validate inputs
    try:
        year = int(year)
        month = int(month)
        if month < 1 or month > 12:
            print(f"DEBUG: Invalid month value: {month}")
            return queryset.none()
    except (ValueError, TypeError) as e:
        print(f"DEBUG: Error converting year/month to int: {e}")
        return queryset.none()

    # Get the start and end dates for the month
    start_date = datetime(year, month, 1).date()
    _, last_day = monthrange(year, month)
    end_date = datetime(year, month, last_day).date()

    print(f"DEBUG: Filtering GLS queryset from {start_date} to {end_date}")
    print(f"DEBUG: Original queryset count: {queryset.count()}")

    # Filter the queryset
    filtered_queryset = queryset.filter(date__gte=start_date, date__lte=end_date)
    print(f"DEBUG: Filtered queryset count: {filtered_queryset.count()}")

    return filtered_queryset


@register.simple_tag
def calculate_gls_total_price(queryset):
    """
    Calculate the total price for GLS services including delivered packages,
    pickup packages, and SHD entries

    Args:
        queryset: A queryset of GLS objects

    Returns:
        dict: A dictionary with detailed pricing information
    """
    delivered_price = calculate_gls_delivered_packages_price(queryset)

    pickup_prices = calculate_gls_pickup_packages_price(queryset)
    pickup_price = pickup_prices['total_price']

    shd_price = calculate_gls_shd_price(queryset)

    total_price = round(delivered_price + pickup_price + shd_price, 2)

    return {
        'delivered_price': delivered_price,
        'pickup_price': pickup_price,
        'regular_pickup_price': pickup_prices['regular_pickup_price'],
        'eo_price': pickup_prices['eo_price'],
        'shd_price': shd_price,
        'total_price': total_price,
    }
