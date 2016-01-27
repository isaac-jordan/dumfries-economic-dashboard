from django.contrib import admin
from models import Datasource, Visualisation, DashboardDataset, SavedConfig, SavedGraph

class DashboardDatasetAdmin(admin.ModelAdmin):
    list_display = DashboardDataset._meta.get_all_field_names()
    
class DatasourceAdmin(admin.ModelAdmin):
    list_display = Datasource._meta.get_all_field_names()
    list_display.remove("visualisation")
    
class VisualisationAdmin(admin.ModelAdmin):
    list_display = Visualisation._meta.get_all_field_names()
    list_display.remove("savedgraph")
    list_display.remove("dashboarddataset")
    
class SavedConfigAdmin(admin.ModelAdmin):
    list_display = SavedConfig._meta.get_all_field_names()
    list_display.remove("savedgraph")
    
class SavedGraphAdmin(admin.ModelAdmin):
    list_display = SavedGraph._meta.get_all_field_names()

admin.site.register(DashboardDataset, DashboardDatasetAdmin)
admin.site.register(Datasource, DatasourceAdmin)
admin.site.register(Visualisation, VisualisationAdmin)
admin.site.register(SavedConfig, SavedConfigAdmin)
admin.site.register(SavedGraph, SavedGraphAdmin)