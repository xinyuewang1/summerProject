from django.shortcuts import render

def index(request):
    return render(request, 'busRoute/index.html', {})

def stops(request):
    return render(request, 'busRoute/stops.html', {})

def tourism(request):
    return render(request, 'busRoute/tourism.html',{})