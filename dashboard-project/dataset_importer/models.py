from django.db import models
import json

class Importer(models.Model):
    name = models.CharField(max_length=100)
    dataJson = models.TextField(blank=True)
    
    def importData(self):
        """Import and return data from this Importer's storage medium. Data is not stored in dataJson field."""
        pass
    
    def importJsonData(self):
        """Import and return JSON data from this Importer's storage medium. Imported data IS stored in dataJson, but not saved by default."""
        pass
    
    class Meta:
        abstract = True
        
class Dataset(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    dataJSON = models.TextField()
    
    def fromJSON(self):
        return json.loads(self.dataJSON)
    
    def __str__(self):
        if self.name:
            return self.name
        return "Imported Dataset " + str(self.pk)