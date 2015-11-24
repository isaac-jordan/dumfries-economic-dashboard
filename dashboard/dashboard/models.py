from django.db import models

class Dataset:
    filename = models.CharField(max_length=100)
    
class Datasource:
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=100)