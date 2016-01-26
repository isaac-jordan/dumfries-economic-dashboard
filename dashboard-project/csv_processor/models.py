from django.db import models
from dataset_importer.models import Importer
import os, csv, collections, json

class CsvFile(Importer):
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
    source = models.URLField()
    
    def importData(self):
        """Returns 2D Python array of the CSV's data"""
        
        return data
    
    def importJsonData(self):
        self.dataJson = json.dumps(self.importData())
        return self.dataJson
    
class Dimension(models.Model):
    TYPE_CHOICES = (
                        ("row", "Row"),
                        ("col", "Column")
    )
    
    DATA_CHOICES = (
                    ("date", "Date"),
                    ("currency", "Currency"),
                    ("numeric", "Numeric"),
                    ("percentage", "Percentage"),
                    ("fraction", "Fraction"),
                    ("text", "Text")
    )
    
    label = models.CharField(max_length=50,
                             help_text=u"The label that appears for this data series in the CSV file.")
    indexForLabel = models.PositiveIntegerField(null=True, blank=True,
                             help_text=u"The row or column index that the label appears in. If blank, you must specify 'index'. \
                             This is orthogonal to the type. E.g. If type is 'Row', then this field is the column index that the label appears in.")
    type = models.CharField(max_length=3,
                            choices=TYPE_CHOICES,
                            default=TYPE_CHOICES[0][0],
                             help_text=u"Whether these indices should be taken as row or column values.")
    index = models.PositiveIntegerField(null=True, blank=True,
                             help_text=u"<OPTIONAL> If data series has no label, this field can specify the index.")
    dataStartIndex = models.PositiveIntegerField(
                             help_text=u"The index of the first cell of interest for this data series.")
    dataEndIndex = models.PositiveIntegerField(
                             help_text=u"The index of the last cell of interest for this data series.")
    dataType = models.CharField(max_length=10,
                            choices=DATA_CHOICES,
                            default=DATA_CHOICES[0][0],
                             help_text=u"The type of data the CSV contains for this data series.")
    makeXaxisOnGraph = models.BooleanField(
                             help_text=u"Select ONE dimension to be used as the X axis.")
    csvFile = models.ForeignKey(CsvFile)
