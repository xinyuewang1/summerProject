from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Testtrip, Busstops
from .forms import routeForm
from .utils import Ett39A
import requests
import json
import datetime
from datetime import date
import calendar
import os
from django.conf import settings

import csv
    
def routes(request):
    weather = query_weather()
    bikes = bikes_query()
    return render(request, 'busRoute/routes.html', {'bikes': bikes, 'weather': weather})
    

class homeView(generic.TemplateView):

    '''Class for index.html page which renders the page, the form and the weather
    *****Does not include autocomplete yet****
    '''

    template_name = "busRoute/index.html"
    context_object_name = 'weather'

    def get_context_data(self):
        context = super().get_context_data()
        context['weather'] = query_weather()
        return context

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        bikes = bikes_query()
        context = {'weather': weather,'bikes': bikes, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = routeForm(request.POST)
        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            #return_time = form.cleaned_data['returnTime']
            depart_date = form.cleaned_data['departDate']
            #return_date = form.cleaned_data['returnDate']
        
        hour = readTimeIn(depart_time)
        day = parseDate(depart_date)
        bikes = bikes_query()
        
        if hour != -1:
            est = Est39A(source_address, destination_address, 0, hour, 'Jan', day)
        else:
            est = "unavailable"

        
        arrival = arrivalTime(depart_time, est)
        weather = query_weather()
        args = {'form': form,'bikes':bikes, 'source': source_address, 'destination': destination_address, 'depart_time': depart_time, 'depart_date': depart_date , 'arrival_time': arrival, 'est': est, 'weather': weather}
        return render(request, "busRoute/result.html", args)


class plannerView(generic.TemplateView):
    '''Class for stops.html page which renders the page, the form and the weather'''

    template_name = "busRoute/planner.html"
    context_object_name = 'weather'

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        bikes = bikes_query()
        bus = DublinBus()
        context = {'weather': weather, 'bikes': bikes,'form': form, 'bus': bus}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = routeForm(request.POST)
        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            #return_time = form.cleaned_data['returnTime']
            depart_date = form.cleaned_data['departDate']
            #return_date = form.cleaned_data['returnDate']

        hour = readTimeIn(depart_time)
        day = parseDate(depart_date)
        bikes = bikes_query()
        bus = DublinBus()
        
        if hour != -1:
            est = Est39A(source_address, destination_address, 0, hour, 'Jan', day)
        else:
            est = "unavailable"

        
        arrival = arrivalTime(depart_time, est)
        weather = query_weather()
        args = {'form': form, 'bikes':bikes, 'source': source_address, 'destination': destination_address, 'depart_time': depart_time, 'depart_date': depart_date , 'arrival_time': arrival, 'est': est, 'weather': weather, 'bus': bus}
        return render(request, "busRoute/result.html", args)


class resultView(generic.TemplateView):
    '''Class for stops.html page which renders the page, the form and the weather'''

    template_name = "busRoute/result.html"
    context_object_name = 'weather'

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        bikes = bikes_query()
        context = {'weather': weather, 'bikes': bikes,'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = routeForm(request.POST)
        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            depart_date = form.cleaned_data['departDate']

        hour = readTimeIn(depart_time)
        day = parseDate(depart_date)
    
        bikes = bikes_query()
        
        if hour != -1:
            est = Est39A(source_address, destination_address, 0, hour, 'Jan', day)
        else:
            est = "unavailable"

        
        arrival = arrivalTime(depart_time, est)
        weather = query_weather()
        args = {'form': form, 'bikes':bikes, 'source': source_address, 'destination': destination_address, 'depart_time': depart_time, 'depart_date': depart_date , 'arrival_time': arrival, 'est': est, 'weather': weather}
        return render(request, self.template_name, args)


class routesView(generic.TemplateView):
    '''Class for routes.html page which renders the page, the form and the weather'''

    template_name = "busRoute/routes.html"
    context_object_name = 'weather'

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        bikes = bikes_query()

        context = {'weather': weather, 'bikes': bikes, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = routeForm(request.POST)
        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
           # return_time = form.cleaned_data['returnTime']
            depart_date = form.cleaned_data['departDate']
           # return_date = form.cleaned_data['returnDate']

        weather = query_weather()
        args = {'form': form, 'source': source_address, 'destination': destination_address, 'depart_time': depart_time, 'depart_date': depart_date , 'weather': weather}
        return render(request, self.template_name, args)

#have to add in weather to this bit, have to set the return to be disabled and add the extra styling and options for the form

def tourism(request):
    return render(request, 'busRoute/tourism.html',{})


def test(request):
    routes = get_route_data()
    return render(request, 'busRoute/test.html',{'routes': routes})


def timeGenerator(request, chosen_time):

    ''''this is a very basic function to display a time chosen'''

    return JsonResponse("You chose %s" % chosen_time, safe=False)



'''these are the more general queries called inside the above classes'''

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
                     'wind': float("{0:.2f}".format(3.6*(r['wind']['speed']))),
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
    #print(web_data.status_code)
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

    '''This function creates a dictionary from the dublin bus data located inside Routes.csv to be accessed on the page for the markers'''

    results = []

    with open(os.path.join(settings.STATIC_ROOT, 'pickles/Routes.csv'), 'r') as f:

        reader = csv.reader(f)

        for i in reader:
               
            
                Info= {'lat': i[2],
                        'lng':i[3],
                        'name': i[1],
                        'num': i[0]
                    }

            
                dbInfo = json.dumps(Info) 
                loadedBikes = json.loads(dbInfo)
                results.append(loadedBikes)
        
    
    return results



def get_route_data(request, route):


    ''''This backend function takes an argument from a url (a route entered in the route info search option) and uses it to query the smart dublin api for its stops information '''

    url = requests.get(f"http://data.dublinked.ie/cgi-bin/rtpi/routeinformation?routeid={route}&operator=bac&format=json")
    url = url.json()

    results = []

    x = url['results'][1]['stops']
  
    for i in x: 
    
    # print(i['latitude'])

        Info= {'lat': i['latitude'],
                        'lng':i['longitude'],
                        'name': i['fullname'],
                        'id': i['stopid']
                        }

        dbInfo = json.dumps(Info) 
        loadedBikes = json.loads(dbInfo)
        results.append(loadedBikes)

    return JsonResponse(results, safe=False)    

             
def GenBusData(request): 


    '''This renders the data to a URL that is used with the AJAX autocomplete function'''


    results = []

    with open(os.path.join(settings.STATIC_ROOT, 'pickles/Routes.csv'), 'r') as f:

        reader = csv.reader(f)

        for i in reader:
               
            
                Info= {'lat': i[2],
                        'lng':i[3],
                        'name': i[1],
                        'num': i[0]
                    }

            
                dbInfo = json.dumps(Info) 
                loadedBikes = json.loads(dbInfo)
                results.append(loadedBikes)
      
    return JsonResponse(results, safe=False) 


def DublinBusRoutes(request):

    '''This function connects to RTPI to get a list of the Routes on Dublin Bus'''

    url = requests.get("https://data.dublinked.ie/cgi-bin/rtpi/routelistinformation?operator=bac&format=json")
    url = url.json()
    results = []
    x = url['results']
    count = 0
  
    for i in x: 
        count += 1

        if count == 352:

            #there was some weird things happening with the api with things called BAC. Will need to find alternative. 
            break
        

        else:   
            
            Info= {'route': i['route']
                    
                    }

            dbInfo = json.dumps(Info) 
            loadedBikes = json.loads(dbInfo)
            results.append(loadedBikes)


    return JsonResponse(results, safe=False) 

              
def Est39A(source, dest, weather, time, month, day):
    ett = Ett39A(source, dest, weather, time, month, day)
    result = ett.estimatedTime()
    result_min = float("{0:.2f}".format(result/60))

    return result_min

def readTimeIn(time):
    try: 
        hour = int(time[0:2])
    except:
        return -1
    return hour

def arrivalTime(depart, travel):

    ''' Function with input parameters depart time and total travel time which returns a string of the arrival time'''

    #Test for correct input
    try: 
        hours = int(depart[0:2])
        mins = int(depart[3:5])
    except:
        return -1
    
    #Converts seconds to hours and minutes
    extra_hours = travel//60
    extra_mins = travel - (extra_hours*60)

    if (mins + extra_mins) > 60:
        extra_hours += 1
        extra_mins -= 60
    
    total_hours = hours + extra_hours

    #Loops to next day
    if (total_hours) >= 24:
        total_hours -= 24
        
    arrival = str(int(total_hours)) + ':' + str(int(mins + extra_mins))
    if arrival[1] == ':':
        final = '0' + arrival
    else:
        final = arrival

    if len(final) == 4:
        return final[0:3] + '0' + final[3]

    return final

def parseDate(d):
    try:
        month, day, year = (int(x) for x in d.split('/'))
        ans = datetime.date(year, month, day)
    except:
        return -1
    return ans.strftime("%A")


def parseTime():
    t = "18:21:41"
    #ti = datetime.datetime.strptime(t, '%H:%M:%S')
    ti = datetime.datetime.now().strftime('%H:%M:%S')
    n = datetime.datetime.now()
    #ti = datetime.datetime.strptime(str(n), '%H:%M:%S')
    c = datetime.datetime.strptime(t, '%H:%M:%S')

    d = datetime.datetime.combine(date.today(), c.time()) - datetime.datetime.combine(date.today(), n.time())
    d = d.__str__()
    return(ti, d)








    

       

      
    




          
                   
                  


