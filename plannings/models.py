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
