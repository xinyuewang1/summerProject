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
import csv
import time
from django.conf import settings
import pandas as pd
    
def problemRend(message):
    form = routeForm()

    context = {'form': form}
    context['error'] = message

    return context
    
class homeView(generic.TemplateView):

    '''Class to render index.html. Includes functions:
        get: Loads the page
        post: Renders the results page for a route plan
    '''

    template_name = "busRoute/index.html" 

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        context = {'weather': weather,'form': form}
        return render(request, self.template_name, context)

    
    def post(self, request):
        form = routeForm(request.POST)
        args = postFunc(request, form)

        return render(request, "busRoute/result.html", args)


class plannerView(generic.TemplateView):
    '''Class to render planner.html page. This is the main page of the web applications with the following functions:
        get: Loads the page
        post: Renders the results page for a route plan
    '''

    template_name = "busRoute/planner.html"

    def get(self,request):

        form = routeForm()
        weather = query_weather()
        context = {'weather': weather, 'form': form}
        
        return render(request, self.template_name, context)
    
    def post(self, request):

        form = routeForm(request.POST)
        args = postFunc(request, form)
        
        if 'problem' in args:
            prob = args['problem']
            b = problemRend(prob)
            return render(request, "busRoute/problem.html", b)

        return render(request, "busRoute/result.html", args)


class resultView(generic.TemplateView):
    '''Class to render template for the route planner results with functions:
        get: Loads the page
        post: Renders the results page for a route plan
    '''

    template_name = "busRoute/result.html"

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        context = {'weather': weather, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):

        form = routeForm(request.POST)
        args = postFunc(request, form)

        return render(request, self.template_name, args)

class problemView(generic.TemplateView):
    '''Class to render template for problems with the form input, with functions:
        get: Loads the page
        post: Renders the results page for a route plan
    '''

    template_name = "busRoute/problem.html"

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        context = {'weather': weather,'form': form}
        return render(request, self.template_name, context)
    

class tourismView(generic.TemplateView):

    '''Class to render index.html. Includes functions:
        get: Loads the page
        post: Renders the results page for a route plan
    '''

    template_name = "busRoute/tourism.html"

    def get(self,request):

        form = routeForm()
        weather = query_weather
        context = {'weather':weather, 'form': form}

        return render(request, self.template_name, context)

    def post(self, request):

        form = routeForm(request.POST)
        args = postFunc(request, form)

        return render(request,"busRoute/result.html" , args)
    
def postFunc(request, form):

    if form.is_valid():
        source_address = form.cleaned_data['source']
        destination_address = form.cleaned_data['destination']
        depart_time = form.cleaned_data['departTime']
        depart_date = form.cleaned_data['departDate']


        #Check for valid time inputs for times that have not already passed and are within a week of current time
        timeChosen = datetime.datetime.strptime(depart_date + " " + depart_time, "%m/%d/%Y %H:%M")
        now = datetime.datetime.now()
        diff = (timeChosen - now).total_seconds() - 3600

        if diff < 0:
            problem = {'problem': "Cannot make a prediction for a past date"}
            return problem
            
        elif diff > 604800:
            problem = {'problem': "Predictions can only be made within a week from today. Please pick a valid date."}
            return problem
    

        #Checking if return values have been given
        try:
            return_time = form.cleaned_data['returnTime']
            return_date = form.cleaned_data['returnDate']
        except:
            pass

    
    #Get travel information from google: Bus and stop numbers
    busNum, legs, source_address1, destination_address1 = googDir(source_address,destination_address, depart_date, depart_time)
    if busNum == -1:
        problem = {'problem': "Error retrieve journey information from Google"}
        return problem

    elif busNum == -2:
        problem = {'problem': "Could not find route for this journey"}
        return problem

    elif busNum == -3:
        problem = {'problem': "Could not find dublin bus route for this journey"}
        return problem
    

    #Get start and end location of full journey by lat lng to plot on the map
    stops_locat = []
    stops_locat.extend(findLatLong(legs[0][1]).split(","))
    stops_locat.extend(findLatLong(legs[len(legs)-1][2]).split(","))

    startLat = stops_locat[0]
    startLng = stops_locat[1]
    finLat = stops_locat[2]
    finLng = stops_locat[3]


    #Other context data: weather, rain, temperature, day (by number), bus and bike markers
    weather = query_weather()
    rain, temp = query_rain_weather(depart_time, depart_date)
    day = parseDayNumber(depart_date)
    bus = DublinBus()

    #Used to find the stop name using a given stop number
    for i in bus:
        if source_address1 == i['num']:
            source_name = i['name']
        if destination_address1 == i['num']:
            destination_name = i['name']

    try:
        source_address = int(source_address)
        destination_address = int(destination_address)

    except:
        for i in bus:
            if source_address == i['name']:
                source_address = i['num']
            if destination_address == i['name']:
                destination_address = i['num']
        

    #Gets date information to be displayed on the prediction result
    dateChosen = datetime.datetime.strptime(depart_date, "%m/%d/%Y")
    header = {'day': calendar.day_name[dateChosen.weekday()],
                    'date': dateChosen.strftime("%d"),
                    'month': dateChosen.strftime("%B")}


    #Finds the estimated travel time for each leg in the journey
    est = 0
    busNum = ""

    for i in legs:

        ett = Est39A(i[0], int(i[1]), int(i[2]), rain, temp, depart_time, day, depart_date)
        try:
            ett = int(ett)
        except:
            problem = {'problem': ett}
            return problem

        #print("ESTimated ", ett)
        est += ett
        busNum += str(i[0] + " ")
    

    #Calculates arrival time based on departure time and estimated length of trip
    arrival = arrivalTime(depart_time, est)

    #Checks for return time and calculates return journey based on the return input information
    if not return_time:
        ert = 0
        pass

    else:
        busNum2, legs2, source_return, destination_return = googDir(destination_address,source_address, return_date, return_time)
        rDay = parseDayNumber(return_date)
        rRain, rTemp = query_rain_weather(return_time, return_date)

        for i in legs:
            ert = int(Est39A(legs2[0][0], int(legs[0][1]), int(legs[0][2]), rRain, rTemp, return_time, day, return_date))
        print("return Time", ert)

    #Return arguments for front end result prediction
    args = {'form': form,'busNum': busNum, 'source': source_address1, 'source_name':source_name, 
    'destination': destination_address1, 'destination_name': destination_name, 'depart_time': depart_time, 
    'depart_date': depart_date , 'arrival_time': arrival, 'startLat':startLat, 'startLng': startLng, 'finLat':finLat,
    'finLng':finLng, 'est': est, 'weather': weather, 'header':header, 'return': ert}

    return args

    
def query_weather():
    """
    Queries Open Weather API for current weather information of Dublin City. Parses input and returns dictionary
    of relevant weather information as well current date and time
    """

    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin&APPID='+os.environ.get('appid'))
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


def bikes_query(request):
    """ 
    Connects to the JCDecaux API and returns the dublin bikes information 
    """
        
    url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey='+os.environ.get('jcdecauxi') # the website containing the data
   
    web_data = requests.get(url)

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

    return JsonResponse(results, safe=False)

def DublinBusInfo(request):
    
    '''
    This function creates a dictionary from the dublin bus data located inside Routes.csv to be accessed on the page for the markers
    '''

    results = []

    with open(os.path.join(settings.STATIC_ROOT, 'pickles/Routes.csv'), 'r', encoding='utf-8') as f:

        reader = csv.reader(f)

        for i in reader:
               
            
                Info= {'lat': i[2],
                        'lng':i[3],
                        'name': i[1],
                        'num': i[0]
                    }

            
                dbInfo = json.dumps(Info) 
                loadedBus = json.loads(dbInfo)
                results.append(loadedBus)
        
    return JsonResponse(results, safe=False)
          
def DublinBus():
    '''
    This function creates a dictionary from the dublin bus data located inside Routes.csv to be accessed on the page for the markers
    '''

    results = []

    with open(os.path.join(settings.STATIC_ROOT, 'pickles/Routes.csv'), 'r', encoding='utf-8') as f:

        reader = csv.reader(f)

        for i in reader:
               
            
                Info= {'lat': i[2],
                        'lng':i[3],
                        'name': i[1],
                        'num': i[0]
                    }

            
                dbInfo = json.dumps(Info) 
                loadedBus = json.loads(dbInfo)
                results.append(loadedBus)
        
    return results


def Db(request, stopid):
    '''
    This accesses the lattitude and longtitude of the chosen source stop for the walk me function
    '''

    results = []
    

    with open(os.path.join(settings.STATIC_ROOT, 'pickles/RouteAdresses.csv'), 'r', encoding='utf-8') as f:

        reader = pd.read_csv(f)
        lat = reader.loc[reader['stopid'] == stopid, 'stop_lat'].values[0]
        lon = reader.loc[reader['stopid'] == stopid, 'stop_lon'].values[0]
    

        Info= {'lat': lat,
                        'lng':lon
                       
                    }
        dbInfo = json.dumps(Info) 
        loadedBus = json.loads(dbInfo)
        results.append(loadedBus)

       
    return JsonResponse(results, safe=False)

                    
def GenBusData(request): 
    '''
    This renders the data to a URL that is used with the AJAX autocomplete function
    '''

    results = []

    with open(os.path.join(settings.STATIC_ROOT, 'pickles/Routes.csv'), 'r', encoding='utf-8') as f:

        reader = csv.reader(f)

        for i in reader:
               
                Info= {'lat': i[2],
                        'lng':i[3],
                        'name': i[1],
                        'num': i[0]
                    }

                dbInfo = json.dumps(Info) 
                loadedBus = json.loads(dbInfo)
                results.append(loadedBus)
      
    return JsonResponse(results, safe=False) 


def stopNearMe(request,lat, lng):


    '''this function is linked to a jQuery which takes the users current lat and long from the geolocation
    This passes this into the google nearby search which returns a list of bus stops near the user. '''

    url = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=500&type=bus_station&key="+os.environ.get('googleapi'))
    url = url.json()

    x = url['results']
    results = []
    for i in x:

        Info= {'name': i['name'],
                'lat': i['geometry']['location']['lat'],
                'long': i['geometry']['location']['lng']
                    
                }

        dbInfo = json.dumps(Info) 
        stopInfo = json.loads(dbInfo)
        results.append(stopInfo)
      

    return JsonResponse(results, safe=False)


def routeDirectionServices(request):


    '''This accesses the routes and directions from a CSV and passs it to a URL that is connected to an AJAX autocomplete function for the Route Search'''

    results = []
  
    with open(os.path.join(settings.STATIC_ROOT, 'pickles/RouteAdresses.csv'), 'r', encoding='utf-8') as f:

        reader = csv.reader(f)
        

        for i in reader:
            Info= {
                        'route': i[5]
                    }
            if Info in results:
                pass
            else:
                dbInfo = json.dumps(Info) 
                routeInfo = json.loads(dbInfo)
                results.append(routeInfo)
        
    return JsonResponse(results, safe=False) 


def get_route_data(request, route):


    ''''This backend function takes an argument from a url (a route entered in the route info search option) and uses it to access the stops on that route using pandas'''


    results = []
    

    with open(os.path.join(settings.STATIC_ROOT, 'pickles/RouteAdresses.csv'), 'r', encoding='utf-8') as f:

        reader = pd.read_csv(f)
        x = reader.loc[reader['direction'] == route ]
        
        if not x.empty: 
            for index, row in x.iterrows(): 
                stop = row['stopid']
                lat = row['stop_lat']
                lng = row['stop_lon']
                name = row['stop_name']

                Info= {'lat': lat,
                                'lng': lng,
                                'name': name,
                                'id': stop
                    }

                dbInfo = json.dumps(Info) 
                routeData = json.loads(dbInfo)
                results.append(routeData)
        else: 

            results = 'fail'
            print(results)

        return JsonResponse(results, safe=False)


def Est39A(route, source, dest, precipitation, temp, timeStr, weekday, dateStr):
    '''
    :param route: route number
    :param source: start stop
    :param dest: end stop
    :param precipitation: precipitation
    :param temp: temperature
    :param timeStr: time picked by user, e.g.:"10:30"
    :param weekday: weekday 0-6
    :param dateStr: date string from user, e.g.: "7/26/2018"
    :return: Estimated travel time
    '''
    ett = Ett39A(route, source, dest, precipitation, temp, timeStr, weekday, dateStr)
    result, error_code = ett.estimatedTime()

    if error_code == -1:
        return result
    elif error_code == -6:
        return result
    else:
        result_min = float("{0:.2f}".format(result / 60))
        return result_min
    
    
def readTimeIn(time):
    '''
    Function to find the hour of a given time input from the front end
    '''

    try: 
        hour = int(time[0:2])
    except:
        return -1

    return hour


def arrivalTime(depart, travel):
    ''' 
    Function with input parameters depart time and total travel time which returns a string of the estimated arrival time
    '''

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


def parseDate(date):
    '''
    Function to return the day of the week with a given date input of form mm/dd/2018
    :return: e.g. "wednesday"
    '''
    try:

        month, day, year = (int(x) for x in date.split('/'))
        ans = datetime.date(year, month, day)

    except:
        return -1

    return ans.strftime("%A")

def parseDayNumber(date):
    '''
    Finds the day of the week as a number 0-6 fmor a given date
    '''
    dt_obj = datetime.datetime.strptime(date, "%m/%d/%Y")
    day = datetime.datetime.weekday(dt_obj)
    return day


def parseTime():
    '''
    Can't remember why I made this function but I know it was important
    It subtracts two times from each other
    '''
    t = "18:21:41"
    ti = datetime.datetime.now().strftime('%H:%M:%S')
    n = datetime.datetime.now()
    c = datetime.datetime.strptime(t, '%H:%M:%S')

    d = datetime.datetime.combine(date.today(), c.time()) - datetime.datetime.combine(date.today(), n.time())
    d = d.__str__()
    return(ti, d)



def query_rain_weather(time, date):
    """
    This function is used to find the rain and temperature value for weather in the future. It takes input
    arguments of the time and date in the future. It then parses to find the hour number and day number with 
    error handling for different sized input strings. It returns two values, rain and temp.
    """
    #Still some issues when it comes to picking times based on the way the api only runs in 3 hour segments so hard
    #to get current time data

    #time = '18:00'
    #date = "7/27/2018"

    if len(date) == 10:
        day = int(date[3:5])
    
    elif len(date) == 8:
        day = int(date[2:3])
    else:
        day = int(date[2:4])
    

    t = int(time[:2])
    
    if t//3 != 0: 
        t= t + (3-(t%3))
    elif t < 3:
        t = 3
    if t > 21:
        t = 21
    

    t = str(t)
  
    r = requests.get('https://api.openweathermap.org/data/2.5/forecast?q=Dublin,IE&appid='+os.environ.get('appid'))
    r = r.json()

    for i in range(0, len(r['list'])):
        
        if str(int(r['list'][i]['dt_txt'][11:13])) == t and int(r['list'][i]['dt_txt'][8:10]) == day:
            
            try:
                rain = r['list'][i]['rain']['3h']
            except:
                
                rain = 0

            temp = float("{0:.2f}".format(r['list'][i]['main']['temp'] -273.15))
            return rain, temp

    raise Exception("Rain and temperature cannot be set for past time")
    

def getRoute(request, bus):
    return JsonResponse(bus, safe=False)



def googDir(origin, dest, date, t):
    """
    Uses googles' direction API to return the bus routes needed for a certain trip
    :param orign: The source address as longitude, latitude string e.g.'53.381131,-6.592682'
    :param dest: The destination address as longitude, latitude string e.g."53.298665 -6.302196"
    :param date: The departure date as a string of form mm/dd/yyyy e.g. "07/28/2018"
    :param t: The departure time as a string of form hh:mm e.g. "11:50"
    :return: An array of the bus route numbers
    """

    #origin = '53.381131,-6.592682'
    #dest = "53.298665 -6.302196"
    #start = "Bray,CountyWicklow,Ireland"
    #end = "Maynooth,CountyKildare,Ireland"
    #tim = "1532785345"
    
    origin = str(origin)
    
    try:
        origin = int(origin)
        dest = int(dest)
        start = findLatLong(str(origin))
        end = findLatLong(str(dest))
        source_stop = str(origin)
        dest_stop = str(dest)
        inputType = "stop" 

    except:
        start = origin.replace(" ", "")
        end = dest.replace(" ", "")
        inputType = "address"
        

    if len(date) == 9:
        date = "0" + date

    buses = []
    legs = []

    #date_str = "07/28/2018 11:50"
    date_str = date + " " + t
    dt_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y %H:%M")
    v = int(time.mktime(dt_obj.timetuple()))

    try:
        b = "&alternatives=true"
        r = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode=transit&departure_time={v}&transit_mode=bus&transit_routing_preference=fewer_transfers&key="+os.environ.get('googleapi'))

    except:
        #raise Exception("Could not find bus route for this journey")
        return -1,-1,-1,-1

    r = r.json()


    try:
        response = r['routes'][0]['legs'][0]['steps']

    except:
        return -2,-2,-2,-2

    #print(response)
    
    if inputType == "address":
        
        for i in response:

            #company = i['transit_details']['line']['agencies'][0]['name']
            
            if i['travel_mode'] == "TRANSIT":
                buses.append(i['transit_details']['line']['short_name'])

                print("goog start", i['start_location']['lat'], ",", i['start_location']['lng'])
                print("goog end", i['end_location']['lat'], ",", i['end_location']['lng'])

                sLat = float("{0:.4f}".format(i['start_location']['lat']))
                sLng = float("{0:.4f}".format(i['start_location']['lng']))

                fLat = float("{0:.4f}".format(i['end_location']['lat']))
                fLng = float("{0:.4f}".format(i['end_location']['lng']))

                startName = i['transit_details']['departure_stop']['name']  
                endName = i['transit_details']['arrival_stop']['name']
                # print()
                # print("GOOGLE JOURNEY DETAILS")
                # print("----------------------")
                # print("Start:", startName, "-- Lat:", sLat, "Long:", sLng)
                # print()
                # print("End:", endName, "-- Lat:", fLat, "Long:", fLng)
                # print()
                # print()

                bus = DublinBus()
            
                for k in range(1,len(bus)):
                    h = bus[k]['lat'][:7]
                    y = bus[k]['lng'][:7]
                    u = bus[k]['name']
                    
                    #if (str(sLat) == h or str(sLng) == y) and startName.startswith(u):
                    if startName.startswith(u):
                        source_stop = bus[k]['num']
                        print("Found 1:", bus[k]['name'])

                       
                    #elif (str(fLat) == h or str(fLng) == y) and endName.startswith(u):
                    elif endName.startswith(u):
                        dest_stop = bus[k]['num']
                        #print(u)
                        print("Found 2:", bus[k]['name'])
                    #print("blah", w, p)
                    b = i['transit_details']['line']['short_name']
                #buses.append(b)
                legs.append([b.upper(), source_stop, dest_stop])
                    
                    

    else:
        for i in response:
            
            if i['travel_mode'] == "TRANSIT":
                b = i['transit_details']['line']['short_name']
                buses.append(b)
                legs.append([b.upper(),source_stop, dest_stop])


    if not buses:
        #raise Exception("No buses available")
        return -3, -3, -3, -3
    
    else:
        print("Bus Numbers:", buses)
        print("legs", legs)
        return buses, legs, source_stop, dest_stop

def findLatLong(location):
    """
    Takes the input of a stop id as a string and returns a string of latitude and longitude separated by a comma
    :param (string): stop_id
    :return (string): latitude, longitude e.g. 53.309418194004,-6.218774829793531
    """
    try:
        stop_id = int(location)

    except:
        address = location
    

    buses = DublinBus()
    if 'stop_id' in locals():
        for b in buses:
            if b['num'] == str(stop_id):
                latLng_str = b['lat'] + "," + b['lng']
                return latLng_str
    else:
        for b in buses:
            if b['name'] == address:
                latLng_str = b['lat'] + "," + b['lng']
                return latLng_str
        
    raise Exception("Unable to find this stop number")

#####Error Pages########

def handler400(request):
    response = render(request, '400.html', context={})
    response.status_code = 400
    return response

def handler401(request):
    response = render(request, '401.html', context={})
    response.status_code = 401
    return response

def handler403(request):
    response = render(request, '403.html', context={})
    response.status_code = 403
    return response

def handler404(request):
    response = render(request, '404.html', context={})
    response.status_code = 404
    return response

def handler408(request):
    response = render(request, '408.html', context={})
    response.status_code = 408
    return response

def handler410(request):
    response = render(request, '410.html', context={})
    response.status_code = 410
    return response

def handler418(request):
    response = render(request, '418.html', context={})
    response.status_code = 418
    return response

def handler421(request):
    response = render(request, '421.html', context={})
    response.status_code = 421
    return response

def handler424(request):
    response = render(request, '424.html', context={})
    response.status_code = 424
    return response

def handler426(request):
    response = render(request, '426.html', context={})
    response.status_code = 426
    return response

def handler429(request):
    response = render(request, '429.html', context={})
    response.status_code = 429
    return response


def handler500(request):
    response = render(request, '500.html', context={})
    response.status_code = 500
    return response
    
def handler501(request):
    response = render(request, '501.html', context={})
    response.status_code = 501
    return response

def handler502(request):
    response = render(request, '502.html', context={})
    response.status_code = 502
    return response

def handler503(request):
    response = render(request, '503.html', context={})
    response.status_code = 503
    return response

def handler504(request):
    response = render(request, '504.html', context={})
    response.status_code = 504
    return response
    
def handler507(request):
    response = render(request, '507.html', context={})
    response.status_code = 507
    return response

def handler508(request):
    response = render(request, '508.html', context={})
    response.status_code = 508
    return response

def handler511(request):
    response = render(request, '511.html', context={})
    response.status_code = 511
    return response

def loaderIO(request):
    f = open(os.path.join(settings.STATIC_ROOT, 'loaderio-0f980bc8a45100d4b616d09b3ef68e68.txt'), 'r', encoding='utf-8')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")



                




