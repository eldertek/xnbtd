from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ExportMixin

from .models import GLS, TNT, Chronopost, Ciblex


# Resource classes for import_export

class GLSResource(resources.ModelResource):
    id = resources.Field(attribute='id')
    name = resources.Field(attribute='name', column_name=_('name'))
    date = resources.Field(attribute='date', column_name=_('date'))
    points_charges = resources.Field(attribute='points_charges', column_name=_('points_charges'))
    points_delivered = resources.Field(
        attribute='points_delivered', column_name=_('points_delivered')
    )
    packages_charges = resources.Field(
        attribute='packages_charges', column_name=_('packages_charges')
    )
    packages_delivered = resources.Field(
        attribute='packages_delivered', column_name=_('packages_delivered')
    )
    avp_relay = resources.Field(attribute='avp_relay', column_name=_('avp_relay'))
    shd = resources.Field(attribute='shd', column_name=_('shd'))
    eo = resources.Field(attribute='eo', column_name=_('eo'))
    pickup_point = resources.Field(attribute='pickup_point', column_name=_('pickup_point'))
    breaks = resources.Field(attribute='breaks', column_name=_('breaks'))
    beginning_hour = resources.Field(attribute='beginning_hour', column_name=_('beginning_hour'))
    ending_hour = resources.Field(attribute='ending_hour', column_name=_('ending_hour'))
    total_hour = resources.Field(attribute='total_hour', column_name=_('total_hour'))

    class Meta:
        model = GLS


class TNTResource(resources.ModelResource):
    id = resources.Field(attribute='id')
    name = resources.Field(attribute='name', column_name=_('name'))
    date = resources.Field(attribute='date', column_name=_('date'))
    client_numbers = resources.Field(attribute='client_numbers', column_name=_('client_numbers'))
    refused = resources.Field(attribute='refused', column_name=_('refused'))
    avp = resources.Field(attribute='avp', column_name=_('avp'))
    cad = resources.Field(attribute='cad', column_name=_('cad'))
    totals_clients = resources.Field(attribute='totals_clients', column_name=_('totals_clients'))
    occasional_abductions = resources.Field(
        attribute='occasional_abductions', column_name=_('occasional_abductions')
    )
    regular_abductions = resources.Field(
        attribute='regular_abductions', column_name=_('regular_abductions')
    )
    totals_clients_abductions = resources.Field(
        attribute='totals_clients_abductions', column_name=_('totals_clients_abductions')
    )
    kilometers = resources.Field(attribute='kilometers', column_name=_('kilometers'))
    breaks = resources.Field(attribute='breaks', column_name=_('breaks'))
    beginning_hour = resources.Field(attribute='beginning_hour', column_name=_('beginning_hour'))
    ending_hour = resources.Field(attribute='ending_hour', column_name=_('ending_hour'))
    total_hour = resources.Field(attribute='total_hour', column_name=_('total_hour'))

    class Meta:
        model = TNT


class ChronopostResource(resources.ModelResource):
    id = resources.Field(attribute='id')
    name = resources.Field(attribute='name', column_name=_('name'))
    date = resources.Field(attribute='date', column_name=_('date'))
    charged_packages = resources.Field(
        attribute='charged_packages', column_name=_('charged_packages')
    )
    charged_points = resources.Field(attribute='charged_points', column_name=_('charged_points'))
    including_ip = resources.Field(attribute='including_ip', column_name=_('including_ip'))
    relay = resources.Field(attribute='relay', column_name=_('relay'))
    return_packages = resources.Field(attribute='return_packages', column_name=_('return_packages'))
    return_points = resources.Field(attribute='return_points', column_name=_('return_points'))
    overdue = resources.Field(attribute='overdue', column_name=_('overdue'))
    anomalies = resources.Field(attribute='anomalies', column_name=_('anomalies'))
    total_points = resources.Field(attribute='total_points', column_name=_('total_points'))
    full_km = resources.Field(attribute='full_km', column_name=_('full_km'))
    breaks = resources.Field(attribute='breaks', column_name=_('breaks'))
    beginning_hour = resources.Field(attribute='beginning_hour', column_name=_('beginning_hour'))
    ending_hour = resources.Field(attribute='ending_hour', column_name=_('ending_hour'))
    total_hour = resources.Field(attribute='total_hour', column_name=_('total_hour'))

    class Meta:
        model = Chronopost


class CiblexResource(resources.ModelResource):
    id = resources.Field(attribute='id')
    name = resources.Field(attribute='name', column_name=_('name'))
    date = resources.Field(attribute='date', column_name=_('date'))
    type = resources.Field(attribute='type', column_name=_('type'))
    code = resources.Field(attribute='code', column_name=_('code'))
    nights = resources.Field(attribute='nights', column_name=_('nights'))
    days = resources.Field(attribute='days', column_name=_('days'))
    avp = resources.Field(attribute='avp', column_name=_('avp'))
    spare_part = resources.Field(attribute='spare_part', column_name=_('spare_part'))
    synchro = resources.Field(attribute='synchro', column_name=_('synchro'))
    morning_pickup = resources.Field(attribute='morning_pickup', column_name=_('morning_pickup'))
    breaks = resources.Field(attribute='breaks', column_name=_('breaks'))
    beginning_hour = resources.Field(attribute='beginning_hour', column_name=_('beginning_hour'))
    ending_hour = resources.Field(attribute='ending_hour', column_name=_('ending_hour'))
    total_hour = resources.Field(attribute='total_hour', column_name=_('total_hour'))

    class Meta:
        model = Ciblex


# Admin classes

class GLSAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = GLSResource
    readonly_fields = ('total_hour',)
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
        'breaks',
        'beginning_hour',
        'ending_hour',
        'total_hour'
    )
    list_filter = ('date', 'name')
    list_statistic = [
        ('total_hour', _('Total Work Hours')),
        ('breaks', _('Total Break Hours')),
        ('packages_delivered', _('Total Packages Delivered')),
    ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


class TNTAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TNTResource
    readonly_fields = ('total_hour',)
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
        'kilometers',
        'breaks',
        'beginning_hour',
        'ending_hour',
        'total_hour'
    )
    list_filter = ('date', 'name')
    list_statistic = [
        ('total_hour', _('Total Work Hours')),
        ('breaks', _('Total Break Hours')),
        ('totals_clients', _('Total Clients')),
    ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


class ChronopostAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ChronopostResource
    readonly_fields = ('total_hour',)
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
        'full_km',
        'breaks',
        'beginning_hour',
        'ending_hour',
        'total_hour'
    )
    list_filter = ('date', 'name')
    list_statistic = [
        ('total_hour', _('Total Work Hours')),
        ('breaks', _('Total Break Hours')),
        ('total_points', _('Total of Points')),
    ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


class CiblexAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CiblexResource
    readonly_fields = ('total_hour',)
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
        'breaks',
        'beginning_hour',
        'ending_hour',
        'total_hour'
    )
    list_filter = ('date', 'name', 'code')
    list_statistic = [
        ('total_hour', _('Total Work Hours')),
        ('breaks', _('Total Break Hours')),
        ('days', _('Total Days'))
    ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_statistic'] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'xnbtd/admin/change_list.html'


admin.site.register(GLS, GLSAdmin)
admin.site.register(TNT, TNTAdmin)
admin.site.register(Chronopost, ChronopostAdmin)
admin.site.register(Ciblex, CiblexAdmin)
