from django.contrib import admin
from models import Datasource, Visualisation, Dataset, SavedConfig, SavedGraph

class DatasetAdmin(admin.ModelAdmin):
    list_display = Dataset._meta.get_all_field_names()
    
class DatasourceAdmin(admin.ModelAdmin):
    list_display = Datasource._meta.get_all_field_names()
    
class VisualisationAdmin(admin.ModelAdmin):
    list_display = Visualisation._meta.get_all_field_names()
    
class SavedConfigAdmin(admin.ModelAdmin):
    list_display = SavedConfig._meta.get_all_field_names()
    
class SavedGraphAdmin(admin.ModelAdmin):
    list_display = SavedGraph._meta.get_all_field_names()

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Datasource, DatasourceAdmin)
admin.site.register(Visualisation, VisualisationAdmin)
admin.site.register(SavedConfig, SavedConfigAdmin)
admin.site.register(SavedGraph, SavedGraphAdmin)