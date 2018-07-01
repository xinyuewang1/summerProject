from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Testtrip
import requests
import json
import datetime
from datetime import date
import calendar

def index(request):
    weather = query_weather()
    context = {'weather': weather}
    return render(request, 'busRoute/index.html', context)
    

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

def query_weather():
    """Queries Open Weather API for current weather information of Dublin City. Parses input and returns dictionary
    of relevant weather information as well current date and time"""
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin&APPID=094f61b4b2da3c4541e43364bab71b0b')
    r = r.json()
    now = datetime.datetime.now()
    my_date = date.today()
    print(r)
    weatherInfo= {'main': r['weather'][0]['main'], 
                     'detail': r['weather'][0]['description'], 
                     'temp': float("{0:.2f}".format(r['main']['temp'] -273.15)),
                     'temp_min': float("{0:.2f}".format(r['main']['temp_min'] - 273.15)),
                     'temp_max': float("{0:.2f}".format(r['main']['temp_max'] - 273.15)),
                     'wind': 3.6*(r['wind']['speed']),
                     'icon': "http://openweathermap.org/img/w/" + str(r['weather'][0]['icon']) + ".png",
                     'day': calendar.day_name[my_date.weekday()],
                     'date': now.strftime("%d"),
                     'month': now.strftime("%B")}
    weatherInfo = json.dumps(weatherInfo)
    loaded_weather = json.loads(weatherInfo)

    return loaded_weather
