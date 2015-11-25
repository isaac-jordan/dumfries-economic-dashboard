import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

import django
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
django.setup()

from dashboard.models import Dataset, Datasource
import json

def populate():
    datasource = add_datasource("test")
    add_dataset(datasource, 'Crime', "bar", [32,13,45,13,12])
    add_dataset(datasource, 'Employment Nature', "bar", [5,3,8,3])
    add_dataset(datasource, 'Unemployment', "bar", [4, 8, 15, 16, 23, 42])
    add_dataset(datasource, 'GDP Per Head ()', "line", [{
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
    add_dataset(datasource, 'Employment Rate', "line", [{
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
    add_dataset(datasource, 'Claimant Count Numbers', "bar", [4, 8, 15, 16, 23, 42])
    add_dataset(datasource, 'House Prices (1000)', "line", [{
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
    add_superuser("test", "test")
    add_user("joe", "test")

def add_dataset(datasource, name, datatype, dataset, html_id="", filename="", sizeX=2, sizeY=1):
    JSONdataset = json.dumps(dataset)
    if html_id == "": 
        html_id = slugify(name)
    p = Dataset.objects.get_or_create(datasource=datasource, name=name, type=datatype, html_id=html_id, dataset=JSONdataset, sizeX=sizeX, sizeY=sizeY)[0]
    p.save()
    return p

def add_datasource(name):
    d = Datasource.objects.get_or_create(name=name)[0]
    return d

def add_user(name, password, email="test@example.com"):
    user = User.objects.create_user(name, email, password)
    return user

def add_superuser(name, password):
    u = User.objects.get_or_create(username=name)[0]
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()
    return u

if __name__ == '__main__':
    print "Starting population script..."
    populate()