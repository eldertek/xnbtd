from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import RestAdminForm
from .models import Event, Rest


# Filters
class StatusFilter(admin.SimpleListFilter):
    title = _('status')  # Human-readable title for the filter
    parameter_name = 'status'  # URL query parameter

    def lookups(self, request, model_admin):
        # Display values for the filter
        return [
            ('validated', _('validated')),
            ('pending', _('pending')),
        ]

    def queryset(self, request, queryset):
        # Modify the queryset based on the filter value
        if self.value() == 'validated':
            return queryset.filter(status=True)
        elif self.value() == 'pending':
            return queryset.filter(status=False)


# Admins
class EventAdmin(admin.ModelAdmin):
    list_filter = ("date",)

    def changelist_view(self, request, extra_context=None):
        self.date_hierarchy = "date"
        self.list_display = ("title", "date")
        return super().changelist_view(request, extra_context)


class RestAdmin(admin.ModelAdmin):
    form = RestAdminForm
    list_display = ("display_status", "linked_user", "start_date", "end_date")
    list_filter = (StatusFilter, "linked_user")

    def display_status(self, obj):
        if obj.status:
            return format_html('<span style="color: green;">{}</span>', _("validated"))
        return format_html('<span style="color: red;">{}</span>', _("pending"))

    display_status.admin_order_field = "status"
    display_status.short_description = _("Status")

    def get_form(self, request, obj=None, **kwargs):
        form = super(RestAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def get_queryset(self, request):
        qs = super(RestAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(RestAdmin, self).get_changeform_initial_data(request)
            get_data["linked_user"] = request.user.pk
            return get_data
        return super(RestAdmin, self).get_changeform_initial_data(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "linked_user":
                kwargs["queryset"] = get_user_model().objects.filter(username=request.user.username)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super(RestAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Event, EventAdmin)
admin.site.register(Rest, RestAdmin)
