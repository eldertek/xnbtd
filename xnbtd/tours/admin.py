from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from .models import BreakTime, GLS, TNT, ChronopostDelivery, ChronopostPickup, Ciblex


class BreakTimeInline(GenericTabularInline):
    model = BreakTime
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 1


class BaseAdmin(admin.ModelAdmin):
    inlines = [BreakTimeInline]
    change_list_template = 'xnbtd/admin/change_list.html'

    def display_breaks(self, obj):
        breaks = BreakTime.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id)
        return ", ".join([str(b.time) for b in breaks])

    display_breaks.short_description = _("Breaks")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super().get_changeform_initial_data(request)
            get_data['linked_user'] = request.user.pk
            return get_data
        return super().get_changeform_initial_data(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "linked_user":
                kwargs["queryset"] = get_user_model().objects.filter(username=request.user.username)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)


class GLSAdmin(BaseAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
        'display_breaks',  
        'license_plate',
        'points_charges',
        'points_delivered',
        'packages_charges',
        'packages_delivered',
        'avp_relay',
        'shd',
        'eo',
        'pickup_point',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [
        ('packages_delivered', _('Total Packages Delivered')),
    ]


class TNTAdmin(BaseAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
        'display_breaks',  
        'license_plate',
        'client_numbers',
        'refused',
        'avp',
        'cad',
        'totals_clients',
        'occasional_abductions',
        'regular_abductions',
        'totals_clients_abductions',
        'kilometers',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [
        ('totals_clients', _('Total Clients')),
    ]


class ChronopostDeliveryAdmin(BaseAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
        'display_breaks',  
        'license_plate',
        'charged_packages',
        'charged_points',
        'including_ip',
        'relay',
        'return_packages',
        'return_points',
        'overdue',
        'anomalies',
        'total_points',
        'full_km',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [
        ('total_points', _('Total of Points')),
    ]


class ChronopostPickupAdmin(BaseAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
        'display_breaks',  
        'license_plate',
        'esd',
        'picked_points',
        'poste',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [
        ('picked_points', _('Total of Picked Points')),
    ]


class CiblexAdmin(BaseAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
        'display_breaks',  
        'license_plate',
        'type',
        'nights',
        'days',
        'avp',
        'spare_part',
        'synchro',
        'morning_pickup',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [('days', _('Total Days'))]


admin.site.register(GLS, GLSAdmin)
admin.site.register(TNT, TNTAdmin)
admin.site.register(ChronopostDelivery, ChronopostDeliveryAdmin)
admin.site.register(ChronopostPickup, ChronopostPickupAdmin)
admin.site.register(Ciblex, CiblexAdmin)
