# Python Library Imports
import json

# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Local Imports
from models import Datasource, Dataset, Visualisation


def home(request):
    return render(request, "index.html")

def graphs(request):
    ds = Datasource.objects.filter(name="test")
    visualisations = Visualisation.objects.filter(dataSource=ds)
    datasets = Dataset.objects.filter(visualisation=visualisations).select_related("visualisation")
    
    widgets = [{'name': o.name,
                           'id': "vis" + str(o.pk),
                           'type': o.type,
                           'dataset': [json.loads(d.dataJSON) for d in datasets.filter(visualisation=o)],
                           'sizeX': o.sizeX,
                           'sizeY': o.sizeY} for o in visualisations]
    
    print(widgets)
    widgets = json.dumps(widgets)
    return render(request, 'pages/graphs.djhtml', { "JSONwidgets": widgets })

def about(request):
    return render(request, 'pages/about.djhtml')

@login_required
def savedConfigs(request):
    return render(request, "pages/savedConfigs.djhtml")

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
    # TODO: implement this

def registrationPage(request):
    return render(request, "pages/register.djhtml")