import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

import django
django.setup()

from dashboard.models import Dataset, Datasource
import json

def populate():
    datasource = add_datasource("test")
    add_dataset(datasource, 'Crime', "bar", "crime", [32,13,45,13,12])
    add_dataset(datasource, 'Employment Nature', "bar", "employment-nature", [5,3,8,3])
    add_dataset(datasource, 'Unemployment', "bar", "unemployment", [4, 8, 15, 16, 23, 42])
    add_dataset(datasource, 'GDP Per Head ()', "line", "gdp", [{
                "y": "152",
                "x": "2000"
            }, {
                "y": "189",
                "x": "2002"
            }, {
                "y": "179",
                "x": "2004"
            }, {
                "y": "199",
                "x": "2006"
            }, {
                "y": "134",
                "x": "2008"
            }, {
                "y": "176",
                "x": "2010"
            }], sizeY=2)
    add_dataset(datasource, 'Employment Rate', "line", "employment-rate", [{
                "y": "152",
                "x": "2000"
            }, {
                "y": "189",
                "x": "2002"
            }, {
                "y": "179",
                "x": "2004"
            }, {
                "y": "199",
                "x": "2006"
            }, {
                "y": "134",
                "x": "2008"
            }, {
                "y": "176",
                "x": "2010"
            }], sizeY=2)
    add_dataset(datasource, 'Claimant Count Numbers', "bar", "claimant", [4, 8, 15, 16, 23, 42])
    add_dataset(datasource, 'House Prices (1000)', "line", "house-prices", [{
                "y": "152",
                "x": "2000"
            }, {
                "y": "189",
                "x": "2002"
            }, {
                "y": "179",
                "x": "2004"
            }, {
                "y": "199",
                "x": "2006"
            }, {
                "y": "134",
                "x": "2008"
            }, {
                "y": "176",
                "x": "2010"
            }], sizeY=2)

def add_dataset(datasource, name, t, html_id, dataset, filename="", sizeX=2, sizeY=1):
    JSONdataset = json.dumps(dataset)
    p = Dataset.objects.get_or_create(datasource=datasource, name=name, type=t, html_id=html_id, dataset=JSONdataset, sizeX=sizeX, sizeY=sizeY)[0]
    p.save()
    return p

def add_datasource(name):
    d = Datasource.objects.get_or_create(name=name)[0]
    return d

if __name__ == '__main__':
    print "Starting population script..."
    populate()