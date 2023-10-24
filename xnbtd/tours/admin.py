from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import GLS, TNT, ChronopostDelivery, ChronopostPickup, Ciblex


class GLSAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
        'license_plate',
        'points_charges',
        'points_delivered',
        'packages_charges',
        'packages_delivered',
        'avp_relay',
        'shd',
        'eo',
        'pickup_point',
        'breaks',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [
        ('packages_delivered', _('Total Packages Delivered')),
    ]

    def get_queryset(self, request):
        qs = super(GLSAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(GLSAdmin, self).get_changeform_initial_data(request)
            get_data['linked_user'] = request.user.pk
            return get_data
        return super(GLSAdmin, self).get_changeform_initial_data(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "linked_user":
                kwargs["queryset"] = get_user_model().objects.filter(username=request.user.username)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super(GLSAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


class TNTAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
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
        'breaks',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [
        ('totals_clients', _('Total Clients')),
    ]

    def get_queryset(self, request):
        qs = super(TNTAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(TNTAdmin, self).get_changeform_initial_data(request)
            get_data['linked_user'] = request.user.pk
            return get_data
        return super(TNTAdmin, self).get_changeform_initial_data(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "linked_user":
                kwargs["queryset"] = get_user_model().objects.filter(username=request.user.username)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super(TNTAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


class ChronopostDeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
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
        'breaks',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [
        ('total_points', _('Total of Points')),
    ]

    def get_queryset(self, request):
        qs = super(ChronopostDeliveryAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(ChronopostDeliveryAdmin, self).get_changeform_initial_data(request)
            get_data['linked_user'] = request.user.pk
            return get_data
        return super(ChronopostDeliveryAdmin, self).get_changeform_initial_data(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "linked_user":
                kwargs["queryset"] = get_user_model().objects.filter(username=request.user.username)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super(ChronopostDeliveryAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


class ChronopostPickupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
        'license_plate',
        'esd',
        'picked_points',
        'poste',
        'breaks',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [
        ('picked_points', _('Total of Picked Points')),
    ]

    def get_queryset(self, request):
        qs = super(ChronopostPickupAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(ChronopostPickupAdmin, self).get_changeform_initial_data(request)
            get_data['linked_user'] = request.user.pk
            return get_data
        return super(ChronopostPickupAdmin, self).get_changeform_initial_data(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "linked_user":
                kwargs["queryset"] = get_user_model().objects.filter(username=request.user.username)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super(ChronopostPickupAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


class CiblexAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'linked_user',
        'date',
        'license_plate',
        'type',
        'nights',
        'days',
        'avp',
        'spare_part',
        'synchro',
        'morning_pickup',
        'breaks',
        'beginning_hour',
        'ending_hour',
        'comments',
    )
    list_filter = ('date', 'linked_user', 'name', 'license_plate')
    list_statistic = [('days', _('Total Days'))]

    def get_queryset(self, request):
        qs = super(CiblexAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(CiblexAdmin, self).get_changeform_initial_data(request)
            get_data['linked_user'] = request.user.pk
            return get_data
        return super(CiblexAdmin, self).get_changeform_initial_data(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "linked_user":
                kwargs["queryset"] = get_user_model().objects.filter(username=request.user.username)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super(CiblexAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


admin.site.register(GLS, GLSAdmin)
admin.site.register(TNT, TNTAdmin)
admin.site.register(ChronopostDelivery, ChronopostDeliveryAdmin)
admin.site.register(ChronopostPickup, ChronopostPickupAdmin)
admin.site.register(Ciblex, CiblexAdmin)
