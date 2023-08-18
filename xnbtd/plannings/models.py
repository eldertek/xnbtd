from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    date = models.DateField(verbose_name=_('Date'))
    title = models.CharField(max_length=100, verbose_name=_('Title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['date']


class Rest(models.Model):
    status = models.BooleanField(verbose_name=_('Status'), default=False)
    linked_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Deliveryman'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'))

    def __str__(self):
        return self.start_date.strftime("%d/%m/%Y") + " - " + self.linked_user.username

    class Meta:
        verbose_name = _('Rest')
        verbose_name_plural = _('Rests')
        ordering = ['start_date']
