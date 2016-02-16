# coding=UTF8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
from csv_processor.fileConverter import findFilePath
import django
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files import File
from csv_processor.models import CsvFile, Dimension
from dashboard.models import Category, Datasource, Visualisation, DashboardDataset
import os, json
django.setup()

from dashboard.models import DashboardDataset, DashboardDatasource, Visualisation, Category
from csv_processor.models import CsvFile, Dimension
import json

def populate():
    datasource = add_datasource("Fake Data Test", "http://example.com")
    crimeCategory = add_category("Crime")
    employmentCategory = add_category("Employment")
    housingCategory = add_category("Housing")
    economyCategory = add_category("Economy")
    healthCategory = add_category("Health")

    crimeVis = add_visualisation(datasource, 'Crime', crimeCategory, "bar", "Location", "Num of Crimes")
    add_dataset(crimeVis, dataset = [{
                "y": 32,
                "x": "Edinburgh"
            }, {
                "y": 13,
                "x": "Glasgow"
            }, {
                "y": 45,
                "x": "London"
            }, {
                "y": 13,
                "x": "Leeds"
            }, {
                "y": 12,
                "x": "Dublin"
            }])

    employmentNatureVis = add_visualisation(datasource, 'Employment Nature', employmentCategory, "bar", "Nature", "Num of Employments")
    add_dataset(employmentNatureVis, dataset = [{
                "y": 5,
                "x": "Edinburgh"
            }, {
                "y": 3,
                "x": "Glasgow"
            }, {
                "y": 8,
                "x": "London"
            }, {
                "y": 3,
                "x": "Leeds"
            }])

    unemploymentVis = add_visualisation(datasource, 'Unemployment', employmentCategory, "bar", "Location", "Num of Unemployments")
    add_dataset(unemploymentVis, dataset = [{
                "y": 4,
                "x": "Edinburgh"
            }, {
                "y": 8,
                "x": "Glasgow"
            }, {
                "y": 15,
                "x": "London"
            }, {
                "y": 16,
                "x": "Leeds"
            }, {
                "y": 23,
                "x": "Dublin"
            }])

    # One graph with two lines
    gdpPCVis = add_visualisation(datasource, 'GDP Per Head (Pounds)', economyCategory, "line", "Year", "GDP Per Head", sizeY=2)
    add_dataset(gdpPCVis, dataset = [{
                "y": 152,
                "x": 2000
            }, {
                "y": 189,
                "x": 2002
            }, {
                "y": 179,
                "x": 2004
            }, {
                "y": 199,
                "x": 2006
            }, {
                "y": 134,
                "x": 2008
            }, {
                "y": 176,
                "x": 2010
            }])
    add_dataset(gdpPCVis, dataset = [{
                "y": 16,
                "x": 2000
            }, {
                "y": 200,
                "x": 2002
            }, {
                "y": 150,
                "x": 2004
            }, {
                "y": 230,
                "x": 2006
            }, {
                "y": 120,
                "x": 2008
            }, {
                "y": 110,
                "x": 2010
            }])

    employmentRateVis = add_visualisation(datasource, 'Employment Rate', employmentCategory, "line", "Year", "Percentage Employed", sizeY=2)
    add_dataset(employmentRateVis, [{
                "y": 20,
                "x": 2000
            }, {
                "y": 30,
                "x": 2002
            }, {
                "y": 50,
                "x": 2004
            }, {
                "y": 70,
                "x": 2006
            }, {
                "y": 80,
                "x": 2008
            }, {
                "y": 25,
                "x": 2010
            }])

    claimantCountVis = add_visualisation(datasource, 'Claimant Count Numbers', economyCategory, "bar", "Location", "Num of Claimants")
    add_dataset(claimantCountVis, [{
                "y": 152,
                "x": "Edinburgh"
            }, {
                "y": 189,
                "x": "Glasgow"
            }, {
                "y": 179,
                "x": "London"
            }, {
                "y": 199,
                "x": "Leeds"
            }, {
                "y": 134,
                "x": "Dublin"
            }, {
                "y": 176,
                "x": "Manchester"
            }])

    housePriceVis = add_visualisation(datasource, 'House Price', housingCategory, "line", "Year", "House Prices (1000)", sizeY=2)
    add_dataset(housePriceVis, [{
                "y": 152,
                "x": 2000
            }, {
                "y": 189,
                "x": 2002
            }, {
                "y": 179,
                "x": 2004
            }, {
                "y": 199,
                "x": 2006
            }, {
                "y": 134,
                "x": 2008
            }, {
                "y": 176,
                "x": 2010
            }])
    
    #Add CSV file data
    realDataSource = add_datasource("Real Data Test", "http://example.com");
    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(basepath, "csv_processor", "static", "csv_processor", "test", "data", "test_real_monthly.csv"))
    f = File(open(filepath))
    csvFile = add_csvFile("CSV Real Monthly Sept 2015", housingCategory, realDataSource, f, "http://example.com")
    add_dimension("Dumfries and Galloway", "row", 2, 151, "currency", "£", False, csvFile, indexForLabel=1)
    add_dimension("Scotland", "row", 2, 151, "currency", "£", False, csvFile, indexForLabel=1)
    add_dimension("Month-Year", "row", 2, 151, "date", "%b-%y", True, csvFile, index=5)
    csvFile.createDashboardInfo()

    
    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "council-stock-testing.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Council Stock", economyCategory, realDataSource, f, "http://statistics.gov.scot/data/council-stock")
    add_dimension("Dumfries", "row", 3, 8, "numeric", "", False, csvFile, indexForLabel=2)
    #add_dimension("Scotland", "row", 3, 8, "numeric", "", False, csvFile, indexForLabel=2) # Does not scale well on graph at all.
    add_dimension("Year", "row", 3, 8, "date", "%Y", True, csvFile, index=8)
    csvFile.createDashboardInfo()

    # realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    # filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "full time employment.csv" ))
    # f = File(open(filepath))
    # csvFile = add_csvFile("Full time Employment", economyCategory, realDataSource, f, "http://statistics.gov.scot/data/full-time-employment")
    # add_dimension("Dumfries and Galloway", "row", 3, 10, "numeric", "", False, csvFile, indexForLabel=2)
    # #add_dimension("Scotland", "row", 3, 8, "numeric", "", False, csvFile, indexForLabel=2) # Does not scale well on graph at all.
    # add_dimension("Year", "row", 3, 10, "date", "%Y", True, csvFile, index=7)
    # csvFile.createDashboardInfo()

    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "energy-consumption.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Energy Consumption", economyCategory, realDataSource, f, "http://statistics.gov.scot/data/energy-consumption")
    add_dimension("Dumfries and Galloway", "row", 3, 11, "numeric", "", False, csvFile, index=28)
    #add_dimension("Scotland", "row", 3, 8, "numeric", "", False, csvFile, indexForLabel=2) # Does not scale well on graph at all.
    add_dimension("Year", "row", 3, 11, "date", "%Y", True, csvFile, index=9)
    csvFile.createDashboardInfo()


    # Add some test users
    add_superuser("test@test.com", "test")
    add_user("joe@test.com", "test")

def add_visualisation(dataSource, name, category, dataType, xLabel, yLabel, filename="", sizeX=2, sizeY=1):
    d = Visualisation.objects.get_or_create(dataSource=dataSource,
                                      name=name,
                                      category=category,
                                      type=dataType,
                                      sizeX=sizeX,
                                      sizeY=sizeY,
                                      xLabel=xLabel,
                                      yLabel=yLabel)[0]
    d.save()
    return d

def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

def add_datasource(name, link):
    d = DashboardDatasource.objects.get_or_create(name=name, link=link)[0]
    return d

def add_dataset(visualisation, dataset={}, JSONdataset="", filename=""):
    if JSONdataset == "":
        JSONdataset = json.dumps(dataset);
    d = DashboardDataset.objects.get_or_create(visualisation=visualisation, filename=filename, dataJSON=JSONdataset)[0]
    return d

def add_user(name, password, email="test@example.com"):
    try:
        user = User.objects.get(username=name, email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(name, email, password)
    return user
    

def add_superuser(name, password):
    u = User.objects.get_or_create(username=name)[0]
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()
    return u

def add_csvFile(visualisationName, category, dataSource, file, source):
    c = CsvFile.objects.get_or_create(name=visualisationName,
                                      visualisationName=visualisationName,
                                      category=category,
                                      dataSource=dataSource,
                                      upload=file,
                                      source=source)[0]
    return c

def add_dimension(label, type, dataStartIndex, dataEndIndex, dataType, dataFormat, makeXaxisOnGraph, csvFile, indexForLabel=None, index=None):
    d = Dimension.objects.get_or_create(label=label,
                                        type=type,
                                        dataStartIndex=dataStartIndex,
                                        dataEndIndex=dataEndIndex,
                                        dataType=dataType,
                                        dataFormat=dataFormat,
                                        makeXaxisOnGraph=makeXaxisOnGraph,
                                        csvFile=csvFile,
                                        indexForLabel=indexForLabel,
                                        index=index)[0]
    return d

def importRealData(fileNames):
     for name in fileNames:
         #findFilePath(name) = {"categoryName":"Employment", "visName": usedName, "visType": "line", "visX": "Year", "visY": fileName, "sizeY": 2, "data": data}
         res = findFilePath(name)
         print res
         if res is None:
             continue
         category = add_category("Employment")
         source = add_datasource("Real Data Test", "http://example.com")
         vis = add_visualisation(source, res["visName"], category, res["visType"], res["visX"], name, sizeY=res["sizeY"])
         for line in res["data"]:
             add_dataset(vis, line)

if __name__ == '__main__':
    print "Starting population script..."
    importRealData(['council-house-sales.csv','child-benefit.csv','births-unmarried.csv','Employment Dumfries and Galloway.csv','Employment Scotland.csv', 'Full-Time Employment Dumfries and Galloway.csv','Full-Time Employment Scotland.csv','wages.csv'])
    populate()

#files updated : hospital-adminssions , council stock , employment, energy consumption, full time employment



