from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class GLS(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Tour Name'))
    date = models.DateField(verbose_name=_('Tour Date'))
    points_charges = models.IntegerField(verbose_name=_('Points Charges'))
    points_delivered = models.IntegerField(verbose_name=_('Points Delivered'))
    packages_charges = models.IntegerField(verbose_name=_('Packages Charges'))
    packages_delivered = models.IntegerField(verbose_name=_('Packages Delivered'))
    avp_relay = models.IntegerField(verbose_name=_('AVP Relay'))
    shd = models.IntegerField(verbose_name=_('SHD'))
    eo = models.IntegerField(verbose_name=_('EO'))
    pickup_point = models.IntegerField(verbose_name=_('Pickup Point'))
    breaks = models.TimeField(verbose_name=_('Breaks'))

    beginning_hour = models.TimeField(verbose_name=_('Beginning Hour'))
    ending_hour = models.TimeField(verbose_name=_('Ending Hour'))
    total_hour = models.FloatField(verbose_name=_('Total Hour'), null=True, blank=True)

    def elapsed_time_hours(self):
        if self.beginning_hour and self.ending_hour:
            begin_datetime = datetime.combine(self.date, self.beginning_hour)
            end_datetime = datetime.combine(self.date, self.ending_hour)

            elapsed_time = end_datetime - begin_datetime
            return elapsed_time.total_seconds() / 3600
        return None

    def save(self, *args, **kwargs):
        self.total_hour = self.elapsed_time_hours()
        super(GLS, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('GLS')
        verbose_name_plural = _('GLS')


class Chronopost(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Tour Name'))
    date = models.DateField(verbose_name=_('Tour Date'))
    charged_packages = models.IntegerField(verbose_name=_('Charged Packages'))
    charged_points = models.IntegerField(verbose_name=_('Charged Points'))
    including_ip = models.IntegerField(verbose_name=_('Including IP'))
    relay = models.IntegerField(verbose_name=_('Relay'))
    return_packages = models.IntegerField(verbose_name=_('Return Packages'))
    return_points = models.IntegerField(verbose_name=_('Return Points'))
    overdue = models.IntegerField(verbose_name=_('Overdue'))
    anomalies = models.IntegerField(verbose_name=_('Anomalies'))
    total_points = models.IntegerField(verbose_name=_('Total Points'))
    full_km = models.IntegerField(verbose_name=_('Full KM'))
    breaks = models.TimeField(verbose_name=_('Breaks'))

    beginning_hour = models.TimeField(verbose_name=_('Beginning Hour'))
    ending_hour = models.TimeField(verbose_name=_('Ending Hour'))
    total_hour = models.FloatField(verbose_name=_('Total Hour'), null=True, blank=True)

    def elapsed_time_hours(self):
        if self.beginning_hour and self.ending_hour:
            begin_datetime = datetime.combine(self.date, self.beginning_hour)
            end_datetime = datetime.combine(self.date, self.ending_hour)

            elapsed_time = end_datetime - begin_datetime
            return elapsed_time.total_seconds() / 3600
        return None

    def save(self, *args, **kwargs):
        self.total_hour = self.elapsed_time_hours()
        super(Chronopost, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Chronopost')
        verbose_name_plural = _('Chronopost')


class TNT(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Tour Name'))
    date = models.DateField(verbose_name=_('Tour Date'))
    client_numbers = models.IntegerField(verbose_name=_('Client numbers'))
    refused = models.IntegerField(verbose_name=_('Refused'))
    avp = models.IntegerField(verbose_name=_('avp'))
    cad = models.IntegerField(verbose_name=_('cad/return'))
    totals_clients = models.IntegerField(verbose_name=_('totals clients'))
    occasional_abductions = models.IntegerField(verbose_name=_('occasional abductions'))
    regular_abductions = models.IntegerField(verbose_name=_('regular abductions'))
    totals_clients_abductions = models.IntegerField(verbose_name=_('total clients abductions'))
    kilometers = models.IntegerField(verbose_name=_('KM/Full'))
    breaks = models.TimeField(verbose_name=_('breaks'))

    beginning_hour = models.TimeField(verbose_name=_('Beginning Hour'))
    ending_hour = models.TimeField(verbose_name=_('Ending Hour'))
    total_hour = models.FloatField(verbose_name=_('Total Hour'), null=True, blank=True)

    def elapsed_time_hours(self):
        if self.beginning_hour and self.ending_hour:
            begin_datetime = datetime.combine(self.date, self.beginning_hour)
            end_datetime = datetime.combine(self.date, self.ending_hour)

            elapsed_time = end_datetime - begin_datetime
            return elapsed_time.total_seconds() / 3600
        return None

    def save(self, *args, **kwargs):
        self.total_hour = self.elapsed_time_hours()
        super(TNT, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('TNT - Fedex')
        verbose_name_plural = _('TNT - Fedex')


class Ciblex(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Tour Name'))
    type = models.CharField(max_length=255, default="LIVRAISONS")

    CODE_CHOICES = [
        ("35011", "35011 - RENNES SUD"),
        ("35020", "35020 - RENNES CHU"),
        ("35022", "35022 - MONTFORT SUR MEU"),
        ("35023", "35023 - PACE - ZI LORIENT"),
    ]

    code = models.CharField(max_length=5, choices=CODE_CHOICES)
    date = models.DateField(verbose_name=_('Tour Date'))
    nights = models.IntegerField(verbose_name=_('nights'))
    days = models.IntegerField(verbose_name=_('days'))
    avp = models.IntegerField(verbose_name=_('avp'))
    spare_part = models.IntegerField(verbose_name=_('spare part'))
    synchro = models.IntegerField(verbose_name=_('synchro'))
    morning_pickup = models.IntegerField(verbose_name=_('morning pickups'))
    breaks = models.TimeField(verbose_name=_('Breaks'))

    beginning_hour = models.TimeField(verbose_name=_('Beginning Hour'))
    ending_hour = models.TimeField(verbose_name=_('Ending Hour'))
    total_hour = models.FloatField(verbose_name=_('Total Hour'), null=True, blank=True)

    def elapsed_time_hours(self):
        if self.beginning_hour and self.ending_hour:
            begin_datetime = datetime.combine(self.date, self.beginning_hour)
            end_datetime = datetime.combine(self.date, self.ending_hour)

            elapsed_time = end_datetime - begin_datetime
            return elapsed_time.total_seconds() / 3600
        return None

    def save(self, *args, **kwargs):
        self.total_hour = self.elapsed_time_hours()
        super(Ciblex, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = _('Ciblex')
        verbose_name_plural = _('Ciblex')
