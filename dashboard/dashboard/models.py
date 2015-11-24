from django.db import models

class Datasource(models.Model):
    name = models.CharField(max_length=100)

class Dataset(models.Model):
    datasource = models.ForeignKey(Datasource)
    filename = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    html_id = models.CharField(max_length=100)
    dataset = models.CharField(max_length=10000)
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()