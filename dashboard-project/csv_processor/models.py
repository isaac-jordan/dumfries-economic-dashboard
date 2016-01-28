from django.db import models
from dataset_importer.models import Importer
import os, csv, collections, json, util, locale
from datetime import datetime

from dashboard.models import Visualisation, DashboardDataset, Category, Datasource

class CsvFile(Importer):
    visualisationName = models.CharField(max_length=150)
    category = models.ForeignKey(Category)
    dataSource = models.ForeignKey(Datasource)
    upload = models.FileField()
    source = models.URLField()
    
    def importData(self):
        """Returns 2D Python array of the CSV's data"""    
        data = []
        xAxisData = []
        dimensions = self.dimensions.all()
        with open(self.upload.path) as csvfile:
            reader = util.UnicodeReader(csvfile, encoding="iso-8859-1")
            for dimension in dimensions:
                csvfile.seek(0)
                localData = []
                if dimension.type == "row":
                    if dimension.index != None:
                        i = dimension.index
                        for row in reader:
                            i -= 1
                            if i == 0:
                                localData = row[dimension.dataStartIndex - 1:dimension.dataEndIndex - 1:]
                                break
                    
                    else:
                        index = 0
                        for row in reader:
                            if row[dimension.indexForLabel - 1] == dimension.label:
                                localData = row[dimension.dataStartIndex:dimension.dataEndIndex:]
                                break;
                            else:
                                index += 1
                else:
                    raise NotImplementedError("No support for Dimension.type of column yet.")
                
                #print "Pre-formatting {0}:".format(dimension.label)
                #print localData
                
                # Format data!
                if dimension.dataType == "date":
                    # Use dimension.format as a strptime to retrieve DateTime object
                    #print "FORMAT: " + dimension.dataFormat
                    localData = [datetime.strptime(d, "%b-%y") for d in localData]
                elif dimension.dataType == "currency":
                    # Use dimension.format to remove currency markers ($)
                    # and cast to float.
                    locale.setlocale(locale.LC_ALL, 'en_GB.UTF8')
                    localData = [locale.atoi(d.replace("\xc2\xa3".decode("UTF8"), "")) for d in localData]
                elif dimension.DataType == "numeric":
                    # Cast data to int or float
                    pass
                #...
                else:
                    pass
                #print "Post formatting:"
                #print localData
                if dimension.makeXaxisOnGraph:
                    xAxisData = localData[:]
                else:
                    data.append(localData)
        
        new = []
        #print data
        # [ [ {"y": 48600.0, "x": 2008.0},  {"y": 48600.0, "x": 2008.0}], [] ]
        for yAxis in data:
            #print "found a yaxis"
            if len(yAxis) != len(xAxisData):
                #print len(yAxis)
                #print len(xAxisData)
                raise NotImplementedError("Axes of different lengths aren't supported yet.")
            l = []
            for y, x in zip(yAxis, xAxisData):
                val = {
                    "x": x,
                    "y": y
                }
                l.append(val)
            new.append(l)
            #print new
        data = new
        return data
    
    def importJsonData(self):
        self.dataJson = json.dumps(self.importData(), cls=util.DatetimeEncoder)
        self.save()
        return self.dataJson
    
    def createDashboardInfo(self):
        vis, created = Visualisation.objects.get_or_create(name=self.visualisationName,
                                                  category=self.category,
                                                  type="line",
                                                  dataSource=self.dataSource,
                                                  sizeX=2,
                                                  sizeY=2,
                                                  xLabel="Placeholder",
                                                  yLabel="Placeholder")
        DashboardDataset.objects.filter(visualisation=vis).delete()
        importedDatasets = self.importData()
        for dataset in importedDatasets:
            DashboardDataset.objects.create(visualisation=vis, dataJSON=json.dumps(dataset, cls=util.DatetimeEncoder))
        self.dataJson = json.dumps(self.importData(), cls=util.DatetimeEncoder)
        self.save()
    
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
    dataFormat = models.CharField(max_length=100,
                            help_text=u"ADVANCED: Specify the format of the data. If dataType is 'date', uses strptime formatting. Otherwise uses Python Regex formatting.")
    makeXaxisOnGraph = models.BooleanField(
                             help_text=u"Select ONE dimension to be used as the X axis.")
    csvFile = models.ForeignKey(CsvFile, related_name='dimensions')