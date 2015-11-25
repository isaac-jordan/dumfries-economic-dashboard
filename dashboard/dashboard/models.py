from django.db import models

class Datasource(models.Model):
    name = models.CharField(max_length=100)
    
class Visualisation(models.Model):
    dataSource = models.ForeignKey(Datasource)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()
    xLabel = models.CharField(max_length=100)
    yLabel = models.CharField(max_length=100)

class Dataset(models.Model):
    visualisation = models.ForeignKey(Visualisation)
    filename = models.CharField(max_length=300)
    dataJSON = models.CharField(max_length=10000)
    