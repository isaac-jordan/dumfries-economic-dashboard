from django.db import models
from dataset_importer.models import Importer
import os, csv, collections, json


class Dimension(models.Model):
    label = models.CharField(max_length=50)
    isRow = models.BooleanField()
    makeXaxis = models.BooleanField()


class CsvFile(Importer):
    filename = models.CharField(max_length=1024)
    folderpath = models.CharField(max_length=1024, null=True)
    importantDimensions = models.ManyToManyField(Dimension)
    
    def importData(self):
        """Returns 2D Python array of the CSV's data"""
        if self.folderpath is None:
            fileDirectory = ''
            found = False
            for root, dirs, files in os.walk(os.getcwd()):
                if self.filename in files:
                    fileDirectory=os.path.join(root, self.filename)
                    found = True
                    break
            
            if not found:
                raise IOError("File '" + self.filename + "' could not be found.")
        else:
            fileDirectory=os.path.join(self.folderpath, self.filename)
        
        with open(fileDirectory) as csvfile:
            reader = csv.DictReader(csvfile)
            newarray=[]
            od = {}
            nextarray=[]
            data = []
            for row in reader:
                newarray.append(row)

        for dict in newarray:
            od = collections.OrderedDict(sorted(dict.items()))
            nextarray.append(od)
        
        data = []
        for dict in nextarray:
            dataset = []
            try:
                for k,v in dict.iteritems():
                    x = float(k[0:4])
                    if (x.is_integer()):
                        x = int(x)
                    
                    y = float(v)
                    if (y.is_integer()):
                        y = int(y)
                    
                    dataset.append({
                        'x':x,
                        'y':y
                    })
            except:
                pass
            data.append(dataset)
            
        return data
    
    def importJsonData(self):
        self.dataJson = json.dumps(self.importData())
        return self.dataJson
