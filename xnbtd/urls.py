from django.contrib import admin
from django.urls import path


admin.site.site_header = "NBTD Transport"
admin.site.site_title = "Portail - NBTD Transport"
admin.site.index_title = "Bienvenue sur le portail des services de NBTD Transport"

urlpatterns = [
    path('', admin.site.urls),
]
