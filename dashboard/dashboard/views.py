# Python Library Imports
import json

# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Local Imports
from models import Datasource, Dataset


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

def savedConfigs(request):
    return render(request, "pages/savedConfigs.djhtml")

def loginPage(request):
    return render(request, "pages/login.djhtml")

def ajax_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
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