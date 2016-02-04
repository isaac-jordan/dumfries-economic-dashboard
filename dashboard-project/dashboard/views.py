# Python Library Imports
import json

# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Local Imports
from models import Datasource, DashboardDataset, Visualisation, SavedConfig, SavedGraph, Category
from csv_processor import util


def home(request):
    return render(request, "dashboard/index.djhtml")

def graphs(request):
    return render(request, 'dashboard/pages/graphs.djhtml')

def ajaxGetGraphs(request):
    ds = Datasource.objects.all()
    visualisations = Visualisation.objects.filter(dataSource=ds)
    datasets = DashboardDataset.objects.filter(visualisation=visualisations).select_related("visualisation")
    widgets = [o.getWidget() for o in visualisations]
    return JsonResponse({"widgets": widgets})

def trends(request, graphName):
    graphName = 'Wages'
    graph = Visualisation.objects.filter(name=graphName)
    datasets = DashboardDataset.objects.filter(visualisation=graph)
    lineNum = 1

    valuesList = []
    for dsObj in datasets:
        values={}
        lines={}
        dataset = json.loads(dsObj.dataJSON)
        maxXPair = dataset[0].copy()
        maxYPair = dataset[0].copy()
        lowestYpair=dataset[0].copy()
        print dataset
        for point in dataset:
            if point["x"] is str:
                dt = json.loads(point["x"], cls=util.DatetimeEncoder)
                if dt > maxXPair['x']:
                    maxXPair=point.copy()
            else:
                year = point["x"]
                if point["x"] > maxXPair["x"]:
                    maxXPair = point.copy()

            if point["y"] > maxYPair["y"]:
                maxYPair = point.copy()
            if point["y"] < lowestYpair["y"]:
                lowestYpair = point.copy()
        print maxXPair
        values["maxX"] = maxXPair.copy()
        values["maxY"] = maxYPair.copy()
        values["lowestY"] = lowestYpair.copy()
        lines["line "+str(lineNum)] = values
        lineNum+=1
        valuesList.append(lines)
    return render(request,'dashboard/pages/category.djhtml', {graphName: valuesList})


    # in form 	[{"y": y value, "x": x value}]
    #for line in dataset:
        #for value in line:

def categoryList(request):
    categories = Category.objects.all()
    print categories
    return render(request, "dashboard/pages/categoryList.djhtml", {"categories": categories})

def category(request, categoryName):
    category = Category.objects.filter(name__iexact=categoryName)
    categoryVis = Visualisation.objects.filter(category=category)
    
    widgets = [];
    datasets = DashboardDataset.objects
    for v in categoryVis:
        widget = {}
        widget["sizeX"] = v.sizeX
        widget["sizeY"] = v.sizeY
        widget["name"] = v.name
        widget["pk"] = v.pk
        widget["type"] = v.type
        widget["dataset"] = [json.loads(d.dataJSON) for d in datasets.filter(visualisation=v)]
        widgets.append(widget)
    
    if category.count() < 1:
        error = "Category '" + categoryName + "' name not found."
    else:
        error = None
        category = category[0]
    return render(request, "dashboard/pages/category.djhtml", {"category": category, "widgets": widgets, "widgetsJSON": json.dumps(widgets), "error": error})

@login_required
def savedConfigs(request):
    configs = SavedConfig.objects.filter(user=request.user)
    return render(request, "dashboard/pages/savedConfigs.djhtml", {"configurations": configs})

#TODO: Optimise database requests
def saveConfig(request):
    dataJSON = request.POST["data"]
    name = request.POST["name"]
    data = json.loads(dataJSON)
    savedConfig = SavedConfig.objects.create(user=request.user, name=name)
    savedConfig.save()
    print data
    for graph in data:
        vis = Visualisation.objects.filter(id=graph["visPK"])[0]
        savedGraph = SavedGraph.objects.create(visualisation=vis, savedConfig=savedConfig, xPosition=graph["xPosition"], yPosition=graph["yPosition"], sizeX=graph["sizeX"], sizeY=graph["sizeY"])
        savedGraph.save()
    return JsonResponse({'message':'Added new Saved Configuration.', "success": True})

def ajaxloadSavedConfig(request):
    scid = request.POST["id"]
    savedConfig = SavedConfig.objects.filter(id=scid)[0]
    savedGraphs = SavedGraph.objects.filter(savedConfig=savedConfig).select_related("visualisation")
    if savedConfig.user != request.user:
        return JsonResponse({'message':'Error: This Saved Configuration does not belong to you.', "success": False})
    
    widgets = [];
    datasets = DashboardDataset.objects
    for graph in savedGraphs:
        widget = {}
        vis = graph.visualisation
        widget["row"] = graph.yPosition
        widget["col"] = graph.xPosition
        widget["sizeX"] = graph.sizeX
        widget["sizeY"] = graph.sizeY
        widget["name"] = vis.name
        widget["id"] = "vis" + str(vis.pk)
        widget["pk"] = vis.pk
        widget["type"] = vis.type
        widget["dataset"] = [json.loads(d.dataJSON) for d in datasets.filter(visualisation=vis)]
        widgets.append(widget)
    return JsonResponse({"widgets": widgets})

def ajaxDeleteSavedConfig(request):
    scid = request.POST["id"]
    savedConfig = SavedConfig.objects.filter(id=scid)[0]
    savedGraphs = SavedGraph.objects.filter(savedConfig=savedConfig).select_related("user")
    if savedConfig.user != request.user:
        return JsonResponse({'message':'Error: This Saved Configuration does not belong to you.', "success": False})
    savedGraphs.delete()
    savedConfig.delete()
    return JsonResponse({'message':'Deleted Saved Configuration.', "success": True})

def loginPage(request):
    return render(request, "dashboard/pages/login.djhtml")

def ajax_login(request):
    username = request.POST.get('email', "")
    password = request.POST.get('password', "")
    user = authenticate(username=username, password=password)
    if request.POST.get("remember", None) is None:
        request.session.set_expiry(0)
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({'message':'Successfully logged in.', "success": True})
        else:
            return JsonResponse({'message':'Error: Account disabled.', "success": False})
    else:
        return JsonResponse({'message':'Error: Invalid login details.', "success": False})

def ajax_isAuthenticated(request):
    return JsonResponse({"is_authenticated": request.user.is_authenticated()})

def logoutUser(request):
    logout(request)
    # Redirect to a success page.
    return redirect("/")

def ajax_register(request):
    username = request.POST['email']
    password = request.POST['password']
    if User.objects.filter(username=username).exists():
        return JsonResponse({'message':'Error: Email address already used.', 'success': False})
    user = User.objects.create_user(username, username, password)
    user.save()
    user = authenticate(username=username, password=password)
    login(request,user)
    return JsonResponse({'message':'Successfully registered. You will now be logged in.', "success": True})

def registrationPage(request):
    return render(request, "dashboard/pages/register.djhtml")
