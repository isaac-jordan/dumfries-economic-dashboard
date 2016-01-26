from django.db import models
from django.contrib.auth.models import User
import json

class Datasource(models.Model):
    name = models.CharField(max_length=100)
    
    def getAllWidgets(self):
        visualisations = Visualisation.objects.filter(dataSource=self)
        widgets = []
        for vis in visualisations:
            widgets.append(vis.getWidget())
        return widgets
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    
class Visualisation(models.Model):
    dataSource = models.ForeignKey(Datasource)
    name = models.CharField(max_length=100)
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

class Dataset(models.Model):
    visualisation = models.ForeignKey(Visualisation)
    filename = models.CharField(max_length=300, blank=True, null=True)
    dataJSON = models.TextField()
    
    def fromJSON(self):
        return json.loads(self.dataJSON)
    
class SavedConfig(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)

class SavedGraph(models.Model):
    visualisation = models.ForeignKey(Visualisation)
    savedConfig = models.ForeignKey(SavedConfig)
    xPosition = models.IntegerField()
    yPosition = models.IntegerField()
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()
    