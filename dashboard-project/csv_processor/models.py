from django.db import models
from dataset_importer.models import Importer
import os, csv, collections

# Create your models here.
class CsvFile(Importer):
    filename = models.CharField(max_length=1024)
    
    def importData(self):
        """Returns 2D Python array of the CSV's data"""
        fileDirectory = ''
        found = False
        for root, dirs, files in os.walk(os.getcwd()):
            if self.filename in files:
                fileDirectory=root + '/' + self.filename
                found = True
                break
        if not found:
            raise FileNotFoundError("File '" + self.filename + "' could not be found.")
        
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
                    dataset.append({
                        'x':float(k[0:4]),
                        'y':float(v)
                    })
            except:
                pass
            data.append(dataset)
            
        return data
    
    def importJsonData(self):
        self.dataJson = importData()
        return self.dataJson