from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

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

    def display_breaks(self, obj):
        breaks = BreakTime.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
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
        entries_html = [f'<span style="white-space: nowrap;">SHD {entry.number} → {entry.value}</span>' for entry in entries]
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
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = "xnbtd/admin/change_list.html"


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
