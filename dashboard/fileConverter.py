import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
import csv
import django
django.setup()
import collections
from dashboard.models import Dataset, Datasource, Visualisation
import json

def add_visualisation(dataSource, name, dataType, xLabel, yLabel, filename="", sizeX=2, sizeY=1):
    d = Visualisation.objects.get_or_create(dataSource=dataSource,
                                      name=name,
                                      type=dataType,
                                      sizeX=sizeX,
                                      sizeY=sizeY,
                                      xLabel=xLabel,
                                      yLabel=yLabel)[0]
    d.save()
    return d

def add_datasource(name):


    d = Datasource.objects.get_or_create(name=name)[0]
    return d

def add_dataset(visualisation, dataset={}, JSONdataset="", filename=""):
    if JSONdataset == "":
        JSONdataset = json.dumps(dataset);
    d = Dataset.objects.get_or_create(visualisation=visualisation, filename=filename, dataJSON=JSONdataset)
    return d





def readConvertAdd(fileName , source):

    print "converting ..."
    with open(fileName) as csvfile:
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
    for dict in nextarray:
        print dict
        dataset = []
        try:
            for k,v in dict.iteritems():
                print 'samo k ',k
                print 'kastnato k ',float(k[0:4])
                dataset.append({
                    'x':float(k[0:4]),
                    'y':float(v)
                })
        except ValueError: print "Reached letter"

        data.append(dataset)
    newName=fileName.split('/')
    usedName=newName[4][0:-4]
    usedName=usedName[:1].upper() + usedName[1:]
    usedName = usedName.replace('-', " ")
    usedName = usedName.replace('_', " ")
    datasource = add_datasource(source)
    gdpPCVis = add_visualisation(datasource, usedName, "line", "Year", fileName, sizeY=2)
    for line in data:
        print line
        add_dataset(gdpPCVis, line)





#fileName = sys.argv[1]
#SourceOf = sys.argv[2]
#if os.path.exists(fileName):
    #print "converting ...."
    #readConvertAdd(fileName,SourceOf)


#readConvertAdd(sys.argv[1],sys.argv[2])


#dataset = {scotland:{'y':2004-Q1,'x':2430600}}
#TO DO CREATE DICTIONARY TO REPRESEN JSON
#EACH ROW





