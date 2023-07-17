from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_filter = ('date',)

    def changelist_view(self, request, extra_context=None):
        self.date_hierarchy = 'date'
        self.list_display = ('title', 'date')
        return super().changelist_view(request, extra_context)


admin.site.register(Event, EventAdmin)
