from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from . models import *

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    can_delete = True
    readonly_fields = ('created_by','created_at','olive_grove',)
    verbose_name_plural = 'note'

class OliveGroveAdmin(LeafletGeoAdmin):
    list_filter = [
         "created_at",
    ]
    list_display = [
         "name",
         "created_at",
         "created_by"
    ]
    search_fields = (
        "name",
        "created_at",
        "created_by"
    )
    inlines = [ NoteInline, ]
    verbose_name_plural = 'Olive Grove'
    readonly_fields = ('created_by','created_at',)
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not change:
                instance.created_by=request.user
            instance.created_by=instance.olive_grove.created_by
            instance.save()
        formset.save_m2m()
    def save_model(self, request, obj, form, change):
        if obj.srid==2100:
            obj.polygon.transform(2100)
            obj.polygon.srid=2100
        if not change:
            obj.created_by=request.user
        obj.save()

admin.site.register(OliveGrove, OliveGroveAdmin)
