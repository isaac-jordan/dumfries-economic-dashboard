from django.db import models
from django.contrib.auth.models import User
import json

from dataset_importer.models import Dataset

class Datasource(models.Model):
    name = models.CharField(max_length=100)
    
    def getAllWidgets(self):
        visualisations = Visualisation.objects.filter(dataSource=self)
        widgets = []
        for vis in visualisations:
            widgets.append(vis.getWidget())
        return widgets
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Visualisation(models.Model):
    dataSource = models.ForeignKey(Datasource)
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category)
    type = models.CharField(max_length=100)
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()
    xLabel = models.CharField(max_length=100)
    yLabel = models.CharField(max_length=100)
    
    def getWidget(self):
        widget = {'name': self.name,
                           'id': "vis" + str(self.pk),
                           'pk': self.pk,
                           'category': self.category,
                           'type': self.type,
                           'dataset': Dataset.objects.filter(visualisation=self)[0].fromJSON(),
                           'sizeX': self.sizeX,
                           'sizeY': self.sizeY}
        return widget
    
    def __str__(self):
        return self.name

class DashboardDataset(Dataset):
    visualisation = models.ForeignKey(Visualisation)
    filename = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        if self.name:
            return self.name
        return "Dashboard Dataset " + str(self.pk)
    
class SavedConfig(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.name

class SavedGraph(models.Model):
    visualisation = models.ForeignKey(Visualisation)
    savedConfig = models.ForeignKey(SavedConfig)
    xPosition = models.IntegerField()
    yPosition = models.IntegerField()
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()
    
    def __str__(self):
        return "Saved Graph " + str(self.pk)
    