from django.db import models
from django.contrib.auth.models import User

class Datasource(models.Model):
    name = models.CharField(max_length=100)
    
    def getAllWidgets(self):
        #TODO
        return
    
class Visualisation(models.Model):
    dataSource = models.ForeignKey(Datasource)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()
    xLabel = models.CharField(max_length=100)
    yLabel = models.CharField(max_length=100)
    
    def getAllWidgets(self):
        #TODO
        return

class Dataset(models.Model):
    visualisation = models.ForeignKey(Visualisation)
    filename = models.CharField(max_length=300)
    dataJSON = models.CharField(max_length=10000)
    
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
    