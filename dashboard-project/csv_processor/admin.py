from django.contrib import admin
from models import CsvFile, Dimension

class DimensionInline(admin.StackedInline):
    model = Dimension
    
class DimensionAdmin(admin.ModelAdmin):
    list_display = ['label', 'type', 'csvFile']
    
class CsvFileAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ DimensionInline ]

admin.site.register(CsvFile, CsvFileAdmin)
admin.site.register(Dimension, DimensionAdmin)