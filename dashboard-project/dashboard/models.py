"""
Specifies all the models used by dashboard app.
Some of the these models are used by other apps 
for convenience.
"""

from django.db import models
from django.contrib.auth.models import User
import json

from dataset_importer.models import Dataset, Datasource

class DashboardDatasource(Datasource):
    """
    A subclass of generic Datasource.
    
    Adds a method to get all the Visualisations for this Datasource.
    """
    
    def getAllWidgets(self):
        """
        Retrieves all visualisations related to this Datasource,
        calls the getWidget method to get a JS friendly-form.
        """
        
        visualisations = Visualisation.objects.filter(dataSource=self)
        widgets = []
        for vis in visualisations:
            widgets.append(vis.getWidget())
        return widgets
    
class Category(models.Model):
    """
    Provides a way of grouping similar Visualisations together.
    """
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Visualisation(models.Model):
    """
    Contains application specific information about how several datasets
    should be displayed together.
    """
    dataSource = models.ForeignKey(Datasource)
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category)
    type = models.CharField(max_length=100)
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()
    xLabel = models.CharField(max_length=100)
    yLabel = models.CharField(max_length=100)
    
    def getWidget(self):
        """
        Returns all the required info for displaying this visualisation.
        """
        widget = {'name': self.name,
                           'id': "vis" + str(self.pk),
                           'pk': self.pk,
                           'category': self.category.name,
                           'type': self.type,
                           'dataset': [json.loads(d.dataJSON) for d in DashboardDataset.objects.filter(visualisation=self)],
                           'sourceName': self.dataSource.name,
                           'sourceLink': self.dataSource.link,
                           'sizeX': self.sizeX,
                           'sizeY': self.sizeY}
        return widget
    
    def __str__(self):
        return self.name

class DashboardDataset(Dataset):
    """
    A subclass of Dataset that includes Dashboard-specific fields.
    """
    
    visualisation = models.ForeignKey(Visualisation)
    filename = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        if self.name:
            return self.name
        return "Dashboard Dataset " + str(self.pk)
    
class SavedConfig(models.Model):
    """
    Provides a umbrella to group several SavedGraphs together
    under one config.
    """
    
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.name

class SavedGraph(models.Model):
    """
    Stores the current size/position of a graph so that it can
    be reproduced later.
    """
    
    visualisation = models.ForeignKey(Visualisation)
    savedConfig = models.ForeignKey(SavedConfig)
    xPosition = models.IntegerField()
    yPosition = models.IntegerField()
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()
    
    def __str__(self):
        return "Saved Graph " + str(self.pk)
    