from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import formats
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    linked_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Deliveryman"))
    name = models.CharField(max_length=255, verbose_name=_("Tour Name"))
    date = models.DateField(verbose_name=_("Tour Date"))
    beginning_hour = models.TimeField(verbose_name=_("Beginning Hour"))
    ending_hour = models.TimeField(verbose_name=_("Ending Hour"))
    license_plate = models.CharField(max_length=7, verbose_name=_("License Plate"))
    comments = models.TextField(verbose_name=_("Comments"), null=True, blank=True)

    def save(self, *args, **kwargs):
        self.license_plate = self.license_plate.upper()
        super(BaseModel, self).save(*args, **kwargs)

    def __str__(self):
        formatted_date = formats.date_format(self.date, format="l j F Y")
        return f"{self.name} - {formatted_date}"

    class Meta:
        abstract = True


class GLS(BaseModel):
    points_charges = models.IntegerField(verbose_name=_("Points Charges"))
    points_delivered = models.IntegerField(verbose_name=_("Points Delivered"))
    packages_charges = models.IntegerField(verbose_name=_("Packages Charges"))
    packages_delivered = models.IntegerField(verbose_name=_("Packages Delivered"))
    avp_relay = models.IntegerField(verbose_name=_("AVP Relay"))
    shd = models.IntegerField(verbose_name=_("SHD"))
    eo = models.IntegerField(verbose_name=_("EO"))
    pickup_point = models.IntegerField(verbose_name=_("Pickup Point"))
    full_km = models.IntegerField(verbose_name=_("Full KM"))

    class Meta:
        verbose_name = _("GLS")
        verbose_name_plural = _("GLS")


class ChronopostDelivery(BaseModel):
    charged_packages = models.IntegerField(verbose_name=_("Charged Packages"))
    charged_points = models.IntegerField(verbose_name=_("Charged Points"))
    including_ip = models.IntegerField(verbose_name=_("Including IP"))
    relay = models.IntegerField(verbose_name=_("Relay"))
    return_packages = models.IntegerField(verbose_name=_("Return Packages"))
    return_points = models.IntegerField(verbose_name=_("Return Points"))
    overdue = models.IntegerField(verbose_name=_("Overdue"))
    anomalies = models.IntegerField(verbose_name=_("Anomalies"))
    total_points = models.IntegerField(verbose_name=_("Total Points"))
    full_km = models.IntegerField(verbose_name=_("Full KM"))

    class Meta:
        verbose_name = _("Chronopost Delivery")
        verbose_name_plural = _("Chronopost Delivery")


class ChronopostPickup(BaseModel):
    esd = models.IntegerField(verbose_name=_("ESD"))
    picked_points = models.IntegerField(verbose_name=_("Picked Points"))
    poste = models.IntegerField(verbose_name=_("Poste"))

    class Meta:
        verbose_name = _("Chronopost Pickup")
        verbose_name_plural = _("Chronopost Pickup")


class TNT(BaseModel):
    client_numbers = models.IntegerField(verbose_name=_("Client numbers"))
    refused = models.IntegerField(verbose_name=_("Refused"))
    avp = models.IntegerField(verbose_name=_("avp"))
    cad = models.IntegerField(verbose_name=_("cad/return"))
    totals_clients = models.IntegerField(verbose_name=_("totals clients"))
    occasional_abductions = models.IntegerField(verbose_name=_("occasional abductions"))
    regular_abductions = models.IntegerField(verbose_name=_("regular abductions"))
    totals_clients_abductions = models.IntegerField(verbose_name=_("total clients abductions"))
    kilometers = models.IntegerField(verbose_name=_("KM/Full"))

    class Meta:
        verbose_name = _("TNT")
        verbose_name_plural = _("TNT")


class Ciblex(BaseModel):
    type = models.CharField(max_length=255, default="LIVRAISONS")
    nights = models.IntegerField(verbose_name=_("nights"))
    days = models.IntegerField(verbose_name=_("days"))
    avp = models.IntegerField(verbose_name=_("avp"))
    spare_part = models.IntegerField(verbose_name=_("spare part"))
    synchro = models.IntegerField(verbose_name=_("synchro"))
    morning_pickup = models.IntegerField(verbose_name=_("morning pickups"))

    class Meta:
        verbose_name = _("Ciblex")
        verbose_name_plural = _("Ciblex")


class BreakTime(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    start_time = models.TimeField(verbose_name=_("Start of Break"))
    end_time = models.TimeField(verbose_name=_("End of Break"))

    def __str__(self):
        return str(_("Break from {} to {}")).format(self.start_time, self.end_time)

    class Meta:
        verbose_name = _("Break Time")
        verbose_name_plural = _("Break Times")
