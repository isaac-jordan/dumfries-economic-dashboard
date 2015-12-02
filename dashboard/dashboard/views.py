# Python Library Imports
import json

# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Local Imports
from models import Datasource, Dataset, Visualisation, SavedConfig, SavedGraph


def home(request):
    return render(request, "index.html")

def graphs(request):
    return render(request, 'pages/graphs.djhtml')

def ajaxGetGraphs(request):
    ds = Datasource.objects.filter(name="test")
    visualisations = Visualisation.objects.filter(dataSource=ds)
    datasets = Dataset.objects.filter(visualisation=visualisations).select_related("visualisation")
    
    widgets = [{'name': o.name,
                           'id': "vis" + str(o.pk),
                           'pk': o.pk,
                           'type': o.type,
                           'dataset': [json.loads(d.dataJSON) for d in datasets.filter(visualisation=o)],
                           'sizeX': o.sizeX,
                           'sizeY': o.sizeY} for o in visualisations]
    
    print(widgets)
    return JsonResponse({"widgets": widgets})

def about(request):
    return render(request, 'pages/about.djhtml')

@login_required
def savedConfigs(request):
    configs = SavedConfig.objects.filter(user=request.user)
    return render(request, "pages/savedConfigs.djhtml", {"configurations": configs})

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
    datasets = Dataset.objects
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
    return render(request, "pages/login.djhtml")

def ajax_login(request):
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if request.POST["remember"] is None:
        request.session.set_expiry(0)
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({'message':'Successfully logged in.', "success": True})
        else:
            return JsonResponse({'message':'Error: Account disabled.', "success": False})
    else:
        return JsonResponse({'message':'Error: Invalid login details.', "success": False})

def logoutUser(request):
    logout(request)
    # Redirect to a success page.
    return redirect("/")

def ajax_register(request):
    print request.POST
    username = request.POST['email']
    password = request.POST['password']
    if User.objects.filter(username=username).exists():
        return JsonResponse({'message':'Error: Email address already used.', 'success': False})
    user = User.objects.create_user(username, username, password)
    user.save()
    return JsonResponse({'message':'Successfully registered.', "success": True})

def registrationPage(request):
    return render(request, "pages/register.djhtml")