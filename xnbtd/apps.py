from django.apps import AppConfig

class XnbtdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = 'xnbtd.admin.AppAdminSite'
    name = 'xnbtd'
