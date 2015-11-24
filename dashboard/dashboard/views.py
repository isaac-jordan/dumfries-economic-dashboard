from django.shortcuts import render
from models import Datasource, Dataset
import json


def home(request):
    return render(request, "index.html")

def graphs(request):
    ds = Datasource.objects.filter(name="test")
    datasets = Dataset.objects.filter(datasource=ds)
    
    widgets = json.dumps( [{'name': o.name,
                           'id': o.html_id,
                           'type': o.type,
                           'dataset': json.loads(o.dataset),
                           'sizeX': o.sizeX,
                           'sizeY': o.sizeY} for o in datasets] )
    
    print(widgets)
    return render(request, 'pages/graphs.djhtml', { "JSONwidgets": widgets })

def about(request):
    return render(request, 'pages/about.djhtml')