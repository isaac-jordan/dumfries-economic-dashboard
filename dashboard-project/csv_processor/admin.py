from django.contrib import admin
from models import CsvFile, Dimension

class CsvFileAdmin(admin.ModelAdmin):
    list_display = CsvFile._meta.get_all_field_names()
    list_display.remove("importantDimensions")
    
class DimensionAdmin(admin.ModelAdmin):
    list_display = Dimension._meta.get_all_field_names()
    list_display.remove("csvfile")

admin.site.register(CsvFile, CsvFileAdmin)
admin.site.register(Dimension, DimensionAdmin)