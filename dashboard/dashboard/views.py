from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def graphs(request):
    return render(request, 'pages/graphs.djhtml')

def about(request):
    return render(request, 'pages/about.djhtml')