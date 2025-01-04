from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import formats


class BaseModel(models.Model):
    linked_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="livreur")
    name = models.CharField(max_length=255, verbose_name="numéro de tournée")
    date = models.DateField(verbose_name="date")
    beginning_hour = models.TimeField(verbose_name="début de la journée")
    ending_hour = models.TimeField(verbose_name="fin de la journée")
    license_plate = models.CharField(max_length=7, verbose_name="Plaque d'immatriculation")
    comments = models.TextField(verbose_name="Commentaires", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.license_plate = self.license_plate.upper()
        super(BaseModel, self).save(*args, **kwargs)

    def __str__(self):
        formatted_date = formats.date_format(self.date, format="l j F Y")
        return f"{self.name} - {formatted_date}"

    class Meta:
        abstract = True


class GLS(BaseModel):
    points_charges = models.IntegerField(verbose_name="Points chargés")
    points_delivered = models.IntegerField(verbose_name="Points livrés")
    packages_charges = models.IntegerField(verbose_name="Colis chargés")
    packages_delivered = models.IntegerField(verbose_name="Colis livrés")
    avp_relay = models.IntegerField(verbose_name="AVP Relais")
    packages_refused = models.IntegerField(verbose_name="Colis refusés", null=True, blank=True)
    eo = models.IntegerField(verbose_name="EO")
    pickup_point = models.IntegerField(verbose_name="Colis ramassés")
    full_km = models.IntegerField(verbose_name="Plein / KM")

    class Meta:
        verbose_name = "GLS"
        verbose_name_plural = "GLS"


class SHDEntry(models.Model):
    gls = models.ForeignKey(
        GLS, on_delete=models.CASCADE, related_name='shd_entries', verbose_name="Tournée GLS"
    )
    number = models.PositiveIntegerField(verbose_name="SHD", editable=False)
    value = models.IntegerField(verbose_name="valeur")

    def save(self, *args, **kwargs):
        if not self.number:
            last_shd = SHDEntry.objects.filter(gls=self.gls).order_by('-number').first()
            self.number = (last_shd.number + 1) if last_shd else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SHD {self.number}: {self.value}"

    class Meta:
        verbose_name = "SHD"
        verbose_name_plural = "SHD"
        ordering = ["number"]
        unique_together = ["gls", "number"]


class ChronopostDelivery(BaseModel):
    charged_packages = models.IntegerField(verbose_name="Colis chargé")
    charged_points = models.IntegerField(verbose_name="Points chargés")
    including_ip = models.IntegerField(verbose_name="Dont IP")
    relay = models.IntegerField(verbose_name="Relais")
    return_packages = models.IntegerField(verbose_name="Retour COLIS")
    return_points = models.IntegerField(verbose_name="Retour POINTS")
    overdue = models.IntegerField(verbose_name="HORS DELAIS")
    anomalies = models.IntegerField(verbose_name="Anomalies")
    total_points = models.IntegerField(verbose_name="Total points")
    full_km = models.IntegerField(verbose_name="Plein / KM")

    class Meta:
        verbose_name = "Chronopost - Livraison"
        verbose_name_plural = "Chronopost - Livraison"


class ChronopostPickup(BaseModel):
    esd = models.IntegerField(verbose_name="ESD")
    picked_points = models.IntegerField(verbose_name="Point ramassés")
    poste = models.IntegerField(verbose_name="Poste")

    class Meta:
        verbose_name = "Chronopost - Ramasse"
        verbose_name_plural = "Chronopost - Ramasse"


class TNT(BaseModel):
    client_numbers = models.IntegerField(verbose_name="Nombres clients")
    refused = models.IntegerField(verbose_name="refuse")
    avp = models.IntegerField(verbose_name="avp")
    cad = models.IntegerField(verbose_name="cad/retour")
    totals_clients = models.IntegerField(verbose_name="totals client")
    occasional_abductions = models.IntegerField(verbose_name="enlèvements occasionnels")
    regular_abductions = models.IntegerField(verbose_name="enlèvements réguliers")
    totals_clients_abductions = models.IntegerField(verbose_name="totals clients enlèvements")
    kilometers = models.IntegerField(verbose_name="KM/Plein")

    class Meta:
        verbose_name = "TNT - Fedex"
        verbose_name_plural = "TNT - Fedex"


class Ciblex(BaseModel):
    type = models.CharField(max_length=255, default="LIVRAISONS")
    nights = models.IntegerField(verbose_name="nuits")
    days = models.IntegerField(verbose_name="jours")
    avp = models.IntegerField(verbose_name="avp")
    spare_part = models.IntegerField(verbose_name="spare part")
    synchro = models.IntegerField(verbose_name="synchro")
    relais = models.IntegerField(verbose_name="relais")
    morning_pickup = models.IntegerField(verbose_name="ramassages matin")

    class Meta:
        verbose_name = "Ciblex"
        verbose_name_plural = "Ciblex"


class BreakTime(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    start_time = models.TimeField(verbose_name="Début de la pause")
    end_time = models.TimeField(verbose_name="Fin de la pause")

    def __str__(self):
        return "Pause de {} à {}".format(self.start_time, self.end_time)

    class Meta:
        verbose_name = "Pause"
        verbose_name_plural = "Pauses"
