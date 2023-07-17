from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlanningsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xnbtd.plannings'
    verbose_name = _('app_plannings_name')
