from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ToursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xnbtd.tours'
    verbose_name = _('app_tours_name')
