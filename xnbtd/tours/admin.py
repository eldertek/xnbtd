from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

from xnbtd.analytics.export import export_route_as_csv, export_single_route_as_csv

from .models import GLS, TNT, BreakTime, ChronopostDelivery, ChronopostPickup, Ciblex, SHDEntry


class BreakTimeInline(GenericTabularInline):
    model = BreakTime
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 1
    fields = ["start_time", "end_time"]


class SHDEntryInline(admin.TabularInline):
    model = SHDEntry
    extra = 1
    fields = ['value']


class BaseAdmin(admin.ModelAdmin):
    inlines = [BreakTimeInline]
    change_list_template = "xnbtd/admin/change_list.html"
    change_form_template = "xnbtd/admin/change_form.html"
    actions = [export_route_as_csv]

    def display_breaks(self, obj):
        breaks = BreakTime.objects.filter(
            content_type=ContentType.objects.get_for_model(obj), object_id=obj.id
        )
        if not breaks:
            return "-"
        breaks_html = [
            f'<span style="white-space: nowrap;">'
            f'{b.start_time.strftime("%H:%M")} - {b.end_time.strftime("%H:%M")}</span>'
            for b in breaks
        ]
        return mark_safe("<br>".join(breaks_html))

    display_breaks.short_description = "Pauses"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super().get_changeform_initial_data(request)
            get_data["linked_user"] = request.user.pk
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
        extra_context["list_statistic"] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    def response_change(self, request, obj):
        """Add custom actions to the change form"""
        if '_export_csv' in request.POST:
            return export_single_route_as_csv(self, request, obj.pk)
        return super().response_change(request, obj)


class GLSAdmin(BaseAdmin):
    inlines = [SHDEntryInline, BreakTimeInline]
    date_hierarchy = "date"
    list_display = (
        "name",
        "linked_user",
        "date",
        "beginning_hour",
        "ending_hour",
        "license_plate",
        "points_charges",
        "points_delivered",
        "packages_charges",
        "packages_delivered",
        "avp_relay",
        "display_shd_entries",
        "eo",
        "pickup_point",
        "display_breaks",
        "comments",
    )
    list_filter = ("date", "linked_user", "name", "license_plate")
    list_statistic = [
        ("packages_delivered", "Total Colis livrés"),
    ]
    search_fields = [
        'linked_user__username',
        'name',
        'date',
        'beginning_hour',
        'ending_hour',
        'license_plate',
        'comments',
        'points_charges',
        'points_delivered',
        'packages_charges',
        'packages_delivered',
        'avp_relay',
        'eo',
        'pickup_point',
        'full_km',
    ]

    def display_shd_entries(self, obj):
        entries = obj.shd_entries.all().order_by('number')
        if not entries:
            return "-"
        entries_html = [
            f'<span style="white-space: nowrap;">SHD {entry.number} → {entry.value}</span>'
            for entry in entries
        ]
        return mark_safe("<br>".join(entries_html))

    display_shd_entries.short_description = "SHD"

    def get_queryset(self, request):
        qs = super(GLSAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(GLSAdmin, self).get_changeform_initial_data(request)
            get_data["linked_user"] = request.user.pk
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
        extra_context["list_statistic"] = self.list_statistic

        # Get date hierarchy information if available
        date_hierarchy_choice = None
        if self.date_hierarchy:
            # Récupérer tous les paramètres GET
            print(f"DEBUG: all GET params: {request.GET}")

            # Vérifier tous les paramètres pour trouver ceux liés à la hiérarchie de dates
            date_params = {}
            for key, value in request.GET.items():
                if key.startswith(f'{self.date_hierarchy}__'):
                    date_part = key.split('__')[1]  # Extraire 'year', 'month', etc.
                    date_params[date_part] = value
                    print(f"DEBUG: Found date param: {date_part} = {value}")

            # Si nous avons à la fois l'année et le mois
            if 'year' in date_params and 'month' in date_params:
                date_hierarchy_choice = {'year': date_params['year'], 'month': date_params['month']}
                print(f"DEBUG: date_hierarchy_choice set to {date_hierarchy_choice}")

                # Ajouter des informations sur les données GLS pour ce mois
                from calendar import monthrange
                from datetime import datetime

                try:
                    year = int(date_params['year'])
                    month = int(date_params['month'])

                    start_date = datetime(year, month, 1).date()
                    _, last_day = monthrange(year, month)
                    end_date = datetime(year, month, last_day).date()

                    # Obtenir les données GLS pour ce mois
                    gls_data = self.model.objects.filter(date__gte=start_date, date__lte=end_date)
                    print(f"DEBUG: Found {gls_data.count()} GLS entries for {month}/{year}")

                    # Ajouter ces informations au contexte
                    extra_context['gls_month_data'] = gls_data
                except (ValueError, TypeError) as e:
                    print(f"DEBUG: Error processing date params: {e}")

        extra_context['date_hierarchy_choice'] = date_hierarchy_choice
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = "xnbtd/admin/gls_change_list.html"


class TNTAdmin(BaseAdmin):
    date_hierarchy = "date"
    list_display = (
        "name",
        "linked_user",
        "date",
        "beginning_hour",
        "ending_hour",
        "license_plate",
        "client_numbers",
        "refused",
        "avp",
        "cad",
        "totals_clients",
        "occasional_abductions",
        "regular_abductions",
        "totals_clients_abductions",
        "kilometers",
        "display_breaks",
        "comments",
    )
    list_filter = ("date", "linked_user", "name", "license_plate")
    list_statistic = [
        ("totals_clients", "Total clients"),
    ]
    search_fields = [
        'linked_user__username',
        'name',
        'date',
        'beginning_hour',
        'ending_hour',
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
    ]

    def get_queryset(self, request):
        qs = super(TNTAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(TNTAdmin, self).get_changeform_initial_data(request)
            get_data["linked_user"] = request.user.pk
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
        extra_context["list_statistic"] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = "xnbtd/admin/change_list.html"


class ChronopostDeliveryAdmin(BaseAdmin):
    date_hierarchy = "date"
    list_display = (
        "name",
        "linked_user",
        "date",
        "beginning_hour",
        "ending_hour",
        "license_plate",
        "charged_packages",
        "charged_points",
        "including_ip",
        "relay",
        "return_packages",
        "return_points",
        "overdue",
        "anomalies",
        "total_points",
        "full_km",
        "display_breaks",
        "comments",
    )
    list_filter = ("date", "linked_user", "name", "license_plate")
    list_statistic = [
        ("total_points", "Total des points"),
    ]
    search_fields = [
        'linked_user__username',
        'name',
        'date',
        'beginning_hour',
        'ending_hour',
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
    ]

    def get_queryset(self, request):
        qs = super(ChronopostDeliveryAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(ChronopostDeliveryAdmin, self).get_changeform_initial_data(request)
            get_data["linked_user"] = request.user.pk
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
        extra_context["list_statistic"] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = "xnbtd/admin/change_list.html"


class ChronopostPickupAdmin(BaseAdmin):
    date_hierarchy = "date"
    list_display = (
        "name",
        "linked_user",
        "date",
        "beginning_hour",
        "ending_hour",
        "license_plate",
        "esd",
        "picked_points",
        "poste",
        "display_breaks",
        "comments",
    )
    list_filter = ("date", "linked_user", "name", "license_plate")
    list_statistic = [
        ("picked_points", "Total des points ramassés"),
    ]
    search_fields = [
        'linked_user__username',
        'name',
        'date',
        'beginning_hour',
        'ending_hour',
        'license_plate',
        'esd',
        'picked_points',
        'poste',
    ]

    def get_queryset(self, request):
        qs = super(ChronopostPickupAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(ChronopostPickupAdmin, self).get_changeform_initial_data(request)
            get_data["linked_user"] = request.user.pk
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
        extra_context["list_statistic"] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = "xnbtd/admin/change_list.html"


class CiblexAdmin(BaseAdmin):
    date_hierarchy = "date"
    list_display = (
        "name",
        "linked_user",
        "date",
        "beginning_hour",
        "ending_hour",
        "license_plate",
        "type",
        "nights",
        "days",
        "avp",
        "spare_part",
        "synchro",
        "relais",
        "morning_pickup",
        "display_breaks",
        "comments",
    )
    list_filter = ("date", "linked_user", "name", "license_plate")
    list_statistic = [
        ("days", "Total jours"),
    ]
    search_fields = [
        'linked_user__username',
        'name',
        'date',
        'beginning_hour',
        'ending_hour',
        'license_plate',
        'type',
        'nights',
        'days',
        'avp',
        'spare_part',
        'synchro',
        'morning_pickup',
    ]

    def get_queryset(self, request):
        qs = super(CiblexAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(linked_user=request.user)

    def get_changeform_initial_data(self, request):
        if not request.user.is_superuser:
            get_data = super(CiblexAdmin, self).get_changeform_initial_data(request)
            get_data["linked_user"] = request.user.pk
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
        extra_context["list_statistic"] = self.list_statistic
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = "xnbtd/admin/change_list.html"


admin.site.register(GLS, GLSAdmin)
admin.site.register(TNT, TNTAdmin)
admin.site.register(ChronopostDelivery, ChronopostDeliveryAdmin)
admin.site.register(ChronopostPickup, ChronopostPickupAdmin)
admin.site.register(Ciblex, CiblexAdmin)
