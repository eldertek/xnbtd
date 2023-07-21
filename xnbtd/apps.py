from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class XnbtdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xnbtd'


class XnbtdAdminConfig(AdminConfig):
    default_site = 'xnbtd.admin.AppAdminSite'
