from django.contrib import admin


class AppAdminSite(admin.AdminSite):
    site_header = "NBTD Transport"
    site_title = "Portail - NBTD Transport"
    index_title = "Bienvenue sur le portail des services de NBTD Transport"
    index_template = "xnbtd/admin/index.html"
