from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from xnbtd.analytics.export import export_route_as_csv

from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = (
        "title",
        "display_license_plate",
        "display_amount",
        "date",
        "linked_user",
    )
    list_filter = ("date", "linked_user", "license_plate")
    search_fields = [
        'title',
        'license_plate',
        'amount',
        'date',
        'linked_user__username',
    ]
    list_statistic = [
        ("amount", "Total des dépenses"),
    ]
    actions = [export_route_as_csv]

    def display_license_plate(self, obj):
        """Format license plate for display"""
        return format_html('<span style="font-weight: bold;">{}</span>', obj.license_plate)

    display_license_plate.short_description = "Plaque d'immatriculation"
    display_license_plate.admin_order_field = "license_plate"

    def display_amount(self, obj):
        """Format amount with currency symbol"""
        return format_html('<span style="color: #e74c3c;">{} €</span>', obj.amount)

    display_amount.short_description = "Montant"
    display_amount.admin_order_field = "amount"

    def get_queryset(self, request):
        qs = super(ExpenseAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(ExpenseAdmin, self).get_changeform_initial_data(request)
            get_data["linked_user"] = request.user.pk
            return get_data
        return super(ExpenseAdmin, self).get_changeform_initial_data(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "linked_user":
                kwargs["queryset"] = get_user_model().objects.filter(username=request.user.username)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super(ExpenseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["list_statistic"] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = "xnbtd/admin/change_list.html"
    change_form_template = "xnbtd/admin/change_form.html"

    def response_change(self, request, obj):
        """Add custom actions to the change form"""
        if '_export_csv' in request.POST:
            from xnbtd.analytics.export import export_single_route_as_csv

            return export_single_route_as_csv(self, request, obj.pk)
        return super().response_change(request, obj)


admin.site.register(Expense, ExpenseAdmin)
