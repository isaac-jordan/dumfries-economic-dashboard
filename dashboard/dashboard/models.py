from django.db import models

class Dataset(models.Model):
    filename = models.CharField(max_length=100)
    
class Datasource(models.Model):
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=100)