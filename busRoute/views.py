from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Testtrip

def index(request):
    return render(request, 'busRoute/index.html', {})

def stops(request):
    return render(request, 'busRoute/stops.html', {})

def tourism(request):
    return render(request, 'busRoute/tourism.html',{})

def timeGenerator(request, chosen_time):

    ''''this is a very basic function to display a time chosen'''

    return JsonResponse("You chose %s" % chosen_time, safe=False)

def detail(request, busroutenum):
    print("Testing stuff")
    all_trips = Testtrip.objects.all()
    html = ''
    for trip in all_trips:
        print(trip)
        html += '<h2>Route number is ' + str(trip.lineid) + '</h2><br>'
    return HttpResponse(html)

