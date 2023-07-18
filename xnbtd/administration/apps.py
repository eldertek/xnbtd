from django.contrib.admin.apps import AdminConfig


class AdministrationConfig(AdminConfig):
    default_site = 'xnbtd.administration.admin.xNBTDAdmin'
