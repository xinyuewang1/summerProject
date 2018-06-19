from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    return render(request, 'busRoute/index.html', {})

def stops(request):
    return render(request, 'busRoute/stops.html', {})

def tourism(request):
    return render(request, 'busRoute/tourism.html',{})

def timeGenerator(request, chosen_time):

    ''''this is a very basic function to display a time chosen'''

    return JsonResponse("You chose %s" % chosen_time, safe=False)
