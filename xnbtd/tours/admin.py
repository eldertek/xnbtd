from django.contrib import admin

from .models import GLS, TNT, Chronopost, Ciblex


class GLSAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'points_charges',
        'points_delivered',
        'packages_charges',
        'packages_delivered',
        'avp_relay',
        'shd',
        'eo',
        'pickup_point',
    )
    list_filter = ('date', 'name')


class TNTAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'client_numbers',
        'refused',
        'avp',
        'cad',
        'totals_clients',
        'occasional_abductions',
        'regular_abductions',
        'totals_clients_abductions',
        'hours',
        'breaks',
        'kilometers',
    )
    list_filter = ('date', 'name')


class ChronopostAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'charged_packages',
        'charged_points',
        'including_ip',
        'relay',
        'return_packages',
        'return_points',
        'overdue',
        'anomalies',
        'total_points',
        'hours',
        'breaks',
        'full_km',
    )
    list_filter = ('date', 'name')


class CiblexAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'type',
        'code',
        'nights',
        'days',
        'avp',
        'spare_part',
        'synchro',
        'morning_pickup',
    )
    list_filter = ('date', 'name', 'code')


admin.site.register(GLS, GLSAdmin)
admin.site.register(TNT, TNTAdmin)
admin.site.register(Chronopost, ChronopostAdmin)
admin.site.register(Ciblex, CiblexAdmin)
