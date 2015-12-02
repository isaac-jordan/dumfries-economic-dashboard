from django.contrib import admin
from models import Dataset, Datasource, Visualisation, SavedConfig, SavedGraph

admin.site.register(Dataset)
admin.site.register(Datasource)
admin.site.register(Visualisation)
admin.site.register(SavedConfig)
admin.site.register(SavedGraph)