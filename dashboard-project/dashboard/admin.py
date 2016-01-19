from django.contrib import admin
from models import Dataset, Datasource, Visualisation, SavedConfig, SavedGraph

class DatasetAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display = ('filename','visualisation')
    
class DatasourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class VisualisationAdmin(admin.ModelAdmin):
    list_display = ('name','category','type','dataSource')
    
class SavedConfigAdmin(admin.ModelAdmin):
    list_display = ('name','user')
    
class SavedGraphAdmin(admin.ModelAdmin):
    list_display = ('savedConfig','visualisation','xPosition', 'yPosition','sizeX','sizeY')

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Datasource, DatasourceAdmin)
admin.site.register(Visualisation, VisualisationAdmin)
admin.site.register(SavedConfig, SavedConfigAdmin)
admin.site.register(SavedGraph, SavedGraphAdmin)