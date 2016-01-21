from django.db import models

class Importer(models.Model):
    name = models.CharField(max_length=100)
    dataJson = models.TextField()
    
    def importData(self):
        """Import and return data from this Importer's storage medium. Data is not stored in dataJson field."""
        pass
    
    def importJsonData(self):
        """Import and return JSON data from this Importer's storage medium. Imported data IS stored in dataJson, but not saved by default."""
        pass
    
    class Meta:
        abstract = True