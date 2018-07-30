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
    

class homeView(generic.TemplateView):

    '''Class to render index.html. Includes functions:
        get: Loads the page
        post: Renders the results page for a route plan
    '''

    template_name = "busRoute/index.html"

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        bikes = bikes_query()
        bus = DublinBus()
        context = {'weather': weather, 'bikes': bikes, 'bus': bus, 'form': form}
        return render(request, self.template_name, context)

    
    def post(self, request):
        form = routeForm(request.POST)

        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            depart_date = form.cleaned_data['departDate']

        
        busNum = googDir(findLatLong(source_address),findLatLong(destination_address), depart_date, depart_time)[0]
        busNum = busNum.upper()

        stops_local = []
        stops_local.extend(findLatLong(source_address).split(","))
        stops_local.extend(findLatLong(destination_address).split(","))

        startLat = stops_local[0]
        startLng = stops_local[1]
        finLat = stops_local[2]
        finLng = stops_local[3]


        weather = query_weather()
        rain, temp = query_rain_weather(depart_time, depart_date)
        day = parseDayNumber(depart_date)
        bus = DublinBus()
        bikes = bikes_query()

        
        #Used to find the stop name using a given stop number
        for i in bus:
            if source_address == i['num']:
                source_name = i['name']
            if destination_address == i['num']:
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
            print("in the except with", source_address, destination_address)
            print("oops")

        dateChosen = datetime.datetime.strptime(depart_date, "%m/%d/%Y")
        #my_date = date.today()
        header = {'day': calendar.day_name[dateChosen.weekday()],
                     'date': dateChosen.strftime("%d"),
                     'month': dateChosen.strftime("%B")}


        #print(source_num, dest_num)
        print("take the bus", busNum)

        #Finds the estimated travel time
        est = Est39A(busNum, int(source_address), int(destination_address), rain, temp, depart_time, day, depart_date)

        #Calculates arrival time based on departure time and estimated length of trip
        arrival = arrivalTime(depart_time, est)

        

        args = {'form': form, 'bikes':bikes, 'bus': bus, 'busNum': busNum, 'source': source_address, 'source_name':source_name, 
        'destination': destination_address, 'destination_name': destination_name, 'depart_time': depart_time, 
        'depart_date': depart_date , 'arrival_time': arrival, 'startLat':startLat, 'startLng': startLng, 'finLat':finLat,
        'finLng':finLng, 'est': est, 'weather': weather, 'header':header}

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
        bikes = bikes_query()
        bus = DublinBus()
        #print(googDir(findLatLong("768"),findLatLong("7161"), "07/28/2018", "11:50"))
        context = {'weather': weather, 'bikes': bikes, 'bus': bus, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):

        form = routeForm(request.POST)

        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            depart_date = form.cleaned_data['departDate']

        
        busNum = googDir(findLatLong(source_address),findLatLong(destination_address), depart_date, depart_time)[0]
        busNum = busNum.upper()

        stops_local = []
        stops_local.extend(findLatLong(source_address).split(","))
        stops_local.extend(findLatLong(destination_address).split(","))

        startLat = stops_local[0]
        startLng = stops_local[1]
        finLat = stops_local[2]
        finLng = stops_local[3]


        weather = query_weather()
        rain, temp = query_rain_weather(depart_time, depart_date)
        day = parseDayNumber(depart_date)
        bus = DublinBus()
        bikes = bikes_query()

        
        #Used to find the stop name using a given stop number
        for i in bus:
            if source_address == i['num']:
                source_name = i['name']
            if destination_address == i['num']:
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
            

        dateChosen = datetime.datetime.strptime(depart_date, "%m/%d/%Y")
        header = {'day': calendar.day_name[dateChosen.weekday()],
                     'date': dateChosen.strftime("%d"),
                     'month': dateChosen.strftime("%B")}

        #print(source_num, dest_num)
        print("take the bus", busNum)

        #Finds the estimated travel time
        est = Est39A(busNum, int(source_address), int(destination_address), rain, temp, depart_time, day, depart_date)

        #Calculates arrival time based on departure time and estimated length of trip
        arrival = arrivalTime(depart_time, est)

        

        args = {'form': form, 'bikes':bikes, 'bus': bus, 'busNum': busNum, 'source': source_address, 'source_name':source_name, 
        'destination': destination_address, 'destination_name': destination_name, 'depart_time': depart_time, 
        'depart_date': depart_date , 'arrival_time': arrival, 'startLat':startLat, 'startLng': startLng, 'finLat':finLat,
        'finLng':finLng, 'est': est, 'weather': weather, 'header':header}

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
        bikes = bikes_query()
        bus = DublinBus()
        context = {'weather': weather, 'bikes': bikes, 'bus':bus, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = routeForm(request.POST)

        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            depart_date = form.cleaned_data['departDate']

        
        busNum = googDir(findLatLong(source_address),findLatLong(destination_address), depart_date, depart_time)[0]
        busNum = busNum.upper()

        stops_local = []
        stops_local.extend(findLatLong(source_address).split(","))
        stops_local.extend(findLatLong(destination_address).split(","))

        startLat = stops_local[0]
        startLng = stops_local[1]
        finLat = stops_local[2]
        finLng = stops_local[3]


        weather = query_weather()
        rain, temp = query_rain_weather(depart_time, depart_date)
        day = parseDayNumber(depart_date)
        bus = DublinBus()
        bikes = bikes_query()

        dateChosen = datetime.datetime.strptime(depart_date, "%m/%d/%Y")
        #my_date = date.today()
        header = {'day': calendar.day_name[dateChosen.weekday()],
                     'date': dateChosen.strftime("%d"),
                     'month': dateChosen.strftime("%B")}

        
        #Used to find the stop name using a given stop number
        for i in bus:
            if source_address == i['num']:
                source_name = i['name']
            if destination_address == i['num']:
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
            print("in the except with", source_address, destination_address)
            print("oops")


        #print(source_num, dest_num)
        print("take the bus", busNum)

        #Finds the estimated travel time
        est = Est39A(busNum, int(source_address), int(destination_address), rain, temp, depart_time, day, depart_date)

        #Calculates arrival time based on departure time and estimated length of trip
        arrival = arrivalTime(depart_time, est)

        

        args = {'form': form, 'bikes':bikes, 'bus': bus, 'busNum': busNum, 'source': source_address, 'source_name':source_name, 
        'destination': destination_address, 'destination_name': destination_name, 'depart_time': depart_time, 
        'depart_date': depart_date , 'arrival_time': arrival, 'startLat':startLat, 'startLng': startLng, 'finLat':finLat,
        'finLng':finLng, 'est': est, 'weather': weather, 'header':header} 
        return render(request, self.template_name, args)

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

        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            depart_date = form.cleaned_data['departDate']

        
        busNum = googDir(findLatLong(source_address),findLatLong(destination_address), depart_date, depart_time)[0]
        busNum = busNum.upper()

        stops_local = []
        stops_local.extend(findLatLong(source_address).split(","))
        stops_local.extend(findLatLong(destination_address).split(","))

        startLat = stops_local[0]
        startLng = stops_local[1]
        finLat = stops_local[2]
        finLng = stops_local[3]


        weather = query_weather()
        rain, temp = query_rain_weather(depart_time, depart_date)
        day = parseDayNumber(depart_date)
        bus = DublinBus()
        bikes = bikes_query()

        
        #Used to find the stop name using a given stop number
        for i in bus:
            if source_address == i['num']:
                source_name = i['name']
            if destination_address == i['num']:
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
            print("in the except with", source_address, destination_address)
            print("oops")


        #print(source_num, dest_num)
        print("take the bus", busNum)

        #Finds the estimated travel time
        est = Est39A(busNum, int(source_address), int(destination_address), rain, temp, depart_time, day, depart_date)

        #Calculates arrival time based on departure time and estimated length of trip
        arrival = arrivalTime(depart_time, est)

        

        args = {'form': form, 'bikes':bikes, 'bus': bus, 'busNum': busNum, 'source': source_address, 'source_name':source_name, 
        'destination': destination_address, 'destination_name': destination_name, 'depart_time': depart_time, 
        'depart_date': depart_date , 'arrival_time': arrival, 'startLat':startLat, 'startLng': startLng, 'finLat':finLat,
        'finLng':finLng, 'est': est, 'weather': weather} 

        return render(request,"busRoute/result.html" , args)
    

'''these are the more general queries called inside the above classes'''

def query_weather():
    """
    Queries Open Weather API for current weather information of Dublin City. Parses input and returns dictionary
    of relevant weather information as well current date and time
    """

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

# def Est39A(source, dest, weather, time, month, day):
#     ett = Ett39A(source, dest, weather, time, month, day)
#     result = ett.estimatedTime()
#     return result

# def AnnEst39A(source, dest, actualArr, rain, day):
#     ett = Ann39A(source, dest, actualArr, rain, day)
#     return ett.estimatedTime()

def bikes_query():
    """ 
    Connects to the JCDecaux API and returns the dublin bikes information 
    """
    
    url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=163a27dc14a77d825fb26c4212d74477642b4469' # the website containing the data
   
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

    return results
          
def DublinBus():
    '''
    This function creates a dictionary from the dublin bus data located inside Routes.csv to be accessed on the page for the markers
    '''

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
    ''''
    This backend function takes an argument from a url (a route) and uses to query the smart dublin api for its route information 
    '''

    url = requests.get(f"http://data.dublinked.ie/cgi-bin/rtpi/routeinformation?routeid={route}&operator=bac&format=json")
    url = url.json()

    results = []
    x = url['results'][1]['stops']
  

    for i in x: 
    
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
    '''
    This renders the data to a URL that is used with the AJAX autocomplete function
    '''

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
    '''
    This function connects to RTPI to get a list of the Routes on Dublin Bus
    '''

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



# def Est39A(source, dest, weather, time, month, day):
#     '''
#     Function to find and format the estimated travel travel time
#     '''

#     ett = Ett39A(source, dest, weather, time, month, day)
#     result = ett.estimatedTime()
#     result_min = float("{0:.2f}".format(result/60))

#     return result_min

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
    result = ett.estimatedTime()
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

    else:
        day = int(date[2:4])
    

    t = int(time[:2])

    if t//3 != 0: 
        t= t + (3-(t%3))
    
    if t == 24:
        t = 0

    t = str(t)
  
    r = requests.get('https://api.openweathermap.org/data/2.5/forecast?q=Dublin,IE&appid=26580fb5867fb2fb6af75662d670dd4c')
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
    print(bus)
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
    #tim = "1532785345"
    if len(date) == 9:
        date = "0" + date

    buses = []

    #date_str = "07/28/2018 11:50"
    date_str = date + " " + t
    dt_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y %H:%M")
    v = int(time.mktime(dt_obj.timetuple()))
    
    try:
        r = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={dest}&mode=transit&departure_time={v}&transit_mode=bus&key=AIzaSyC_TopsrUXWcqAxGDfmmbpJzAbZWyVx_s0")
    except:
        raise Exception("Could not find bus route for this journey")

    r = r.json()
    response = r['routes'][0]['legs'][0]['steps']
    for i in response:
        try:
            buses.append(i['transit_details']['line']['short_name'])
        except:
            pass
    if not buses:
        raise Exception("No buses available")
    else:
        return buses 

def findLatLong(location):
    """
    Takes the input of a stop id as a string and returns a string of latitude and longitude separated by a comma
    :param (string): stop_id
    :return (string): latitude, longitude e.g. 53.309418194004,-6.218774829793531
    """
    try:
        stop_id = int(location)
        print(stop_id)
    except:
        address = location
        print(address)

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

