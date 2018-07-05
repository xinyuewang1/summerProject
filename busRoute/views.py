from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Testtrip
from .models import Busstops
import requests
import json
import datetime
from datetime import date
import calendar

def getSource(request):

        '''This function performs the query to find the matches to the users input in the source search bar'''

        if request.is_ajax():
            q = request.GET.get('term', '')
            places = Busstops.objects.filter(stop_id__icontains=q)
            results = []
            for pl in places:
                place_json = {}
                place_json = pl.stop_id
                if place_json in results:
                    pass
                else: 
                    results.append(place_json)
                data = json.dumps(results)
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


def getDestination(request):

        '''This function performs the query to find the matches to the users input in the destination search bar'''


        if request.is_ajax():
            q = request.GET.get('term', '')
            places = Busstops.objects.filter(stop_id__icontains=q)
            results = []
            for pl in places:
                place_json = {}
                place_json = pl.stop_id
                if place_json in results:
                    pass
                else: 
                    results.append(place_json)
                data = json.dumps(results)
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)



def getAddressSource(request):


    '''this function returns the addresses that match the users input into the source input on the routes page'''


    if request.is_ajax():
            q = request.GET.get('term', '')
            places = Busstops.objects.filter(stop_name__icontains=q)
            results = []
            for pl in places:
                place_json = {}
                place_json = pl.stop_name
                if place_json in results:
                    pass
                else: 
                    results.append(place_json)
                data = json.dumps(results)
    else:
            data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



def getAddressDestination(request):


    '''this function returns the addresses that match the users input into the destination input on the routes page'''

    if request.is_ajax():
            q = request.GET.get('term', '')
            places = Busstops.objects.filter(stop_name__icontains=q)
            results = []
            for pl in places:
                place_json = {}
                place_json = pl.stop_name
                if place_json in results:
                    pass
                else: 
                    results.append(place_json)
                data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def index(request):
    weather = query_weather()
    bikes = bikes_query()
    bus = DublinBus()
    context = {'weather': weather, 'bikes': bikes, 'bus': bus}
    return render(request, 'busRoute/index.html', context)
    
def stops(request):
    return render(request, 'busRoute/stops.html', {})

def routes(request):
    return render(request, 'busRoute/routes.html', {})

def tourism(request):
    return render(request, 'busRoute/tourism.html',{})

def timeGenerator(request, chosen_time):

    ''''this is a very basic function to display a time chosen'''

    return JsonResponse("You chose %s" % chosen_time, safe=False)

# def detail(request, busroutenum):
#     print("Testing stuff")
#     all_trips = Testtrip.objects.all()
#     html = ''
#     for trip in all_trips:
#         print(trip)
#         html += '<h2>Route number is ' + str(trip.lineid) + '</h2><br>'
#     return HttpResponse(html)

def query_weather():

    """Queries Open Weather API for current weather information of Dublin City. Parses input and returns dictionary
    of relevant weather information as well current date and time"""
    
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin&APPID=094f61b4b2da3c4541e43364bab71b0b')
    r = r.json()
    now = datetime.datetime.now()
    my_date = date.today()
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

     
def bikes_query():
    
    """ Connects to the JCDecaux API and returns the dublin bikes information """
    
    url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=163a27dc14a77d825fb26c4212d74477642b4469' # the website containing the data
  
   
    web_data = requests.get(url)
    print(web_data.status_code)
    if web_data.status_code == 200:
        data = json.loads(web_data.text)
        results = []
        for i in range(104):
           
            Info= {'lat': data[i]['position']['lat'],
                     'lng': data[i]['position']['lng'], 
                     'name': data[i]['name']
                    
                }
     
            dbInfo = json.dumps(Info)    
            loadedBikes = json.loads(dbInfo)
            results.append(loadedBikes)

    return results
        
    
def DublinBus():

    '''this function creates a dictionary from the dublin bus data to be accessed on the page'''

    data = Busstops.objects.all()
    results = []
    for i in data:

        Info= {'lat': i.stop_lat,
                     'lng':i.stop_lon, 
                     'name': i.stop_name
                    }
        dbInfo = json.dumps(Info) 
        loadedBikes = json.loads(dbInfo)
        results.append(loadedBikes)

    return results


