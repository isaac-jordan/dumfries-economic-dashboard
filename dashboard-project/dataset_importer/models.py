from django.db import models

class Importer(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        abstract = True