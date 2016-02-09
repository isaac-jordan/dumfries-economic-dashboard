"""
This file is here for utility purposes.
It is used my populate.py to process CSV files without hitting the database.
"""

import os
import csv
import collections
import json

def findFilePath(nameFile):
    """
    Locates the first file with the provided name.
    Executes a breadth-first search from current working directory.
    
    Calls realConvertAdd if it finds a file with the name.
    """
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
    """
    Function that actually opens the CSV and constructs
    the data contained within in a nested list.
    """
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
            print ''
        data.append(dataset)
        
    newName=fileName.split('/')
    usedName=newName[len(newName)-1][0:-4]
    usedName=usedName[:1].upper() + usedName[1:]
    usedName = usedName.replace('-', " ")
    usedName = usedName.replace('_', " ")
    
    return {"visName": usedName, "visType": "line", "visX": "Year", "visY": fileName, "sizeY": 2, "data": data}




