import os
import csv
import collections
import json

def findFilePath(nameFile):
    fileDirectory = ''
    found = False
    for root, dirs, files in os.walk(os.getcwd()):
        if nameFile in files:
            fileDirectory=root + '/' + nameFile
            found = True
            break
    if found:
        return readConvertAdd(fileDirectory)
    else: 
        print "file does not exist"
        return None

def readConvertAdd(fileName):
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
        dataset = []
        try:
            for k,v in dict.iteritems():
                dataset.append({
                    'x':float(k[0:4]),
                    'y':float(v)
                })
        except:
            print ''
        data.append(dataset)
        
    newName=fileName.split('/')
    usedName=newName[len(newName)-1][0:-4]
    usedName=usedName[:1].upper() + usedName[1:]
    usedName = usedName.replace('-', " ")
    usedName = usedName.replace('_', " ")
    
    return {"visName": usedName, "visType": "line", "visX": "Year", "visY": fileName, "sizeY": 2, "data": data}
    #datasource = add_datasource(source)
    #category = add_category("Employment")
    #gdpPCVis = add_visualisation(datasource, usedName, category, "line", "Year", fileName, sizeY=2)
    #for line in data:
    #    add_dataset(gdpPCVis, line)





#fileName = sys.argv[1]
#SourceOf = sys.argv[2]
#if os.path.exists(fileName):
    #print "converting ...."
    #readConvertAdd(fileName,SourceOf)


#readConvertAdd(sys.argv[1],sys.argv[2])


#dataset = {scotland:{'y':2004-Q1,'x':2430600}}
#TO DO CREATE DICTIONARY TO REPRESEN JSON
#EACH ROW





