from django.contrib import admin
from models import CsvFile, Dimension

class DimensionInline(admin.StackedInline):
    model = Dimension
    
class DimensionAdmin(admin.ModelAdmin):
    list_display = ['label', 'type', 'csvFile']
    
    def save_related(self, request, form, formsets, change):
        obj = form.instance
        print obj
        print obj.csvFile
        # whatever your formset dependent logic is to change obj.filedata
        obj.save()
        super(CsvFileAdmin, self).save_related(request, form, formsets, change)
    
class CsvFileAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ DimensionInline ]
    
    def save_related(self, request, form, formsets, change):
        obj = form.instance
        super(CsvFileAdmin, self).save_related(request, form, formsets, change)
        obj.importJsonData()
    
    def save_model(self, request, obj, form, change):
        admin.ModelAdmin.save_model(self, request, obj, form, change)
    

admin.site.register(CsvFile, CsvFileAdmin)
admin.site.register(Dimension, DimensionAdmin)