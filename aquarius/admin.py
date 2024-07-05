from django.contrib import admin
from aquarius.models import City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # list_filter = ('field1', 'field4')
    search_fields = ('name',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['additional_data'] = 'This is some additional data'
        
        return super().changelist_view(request, extra_context=extra_context)