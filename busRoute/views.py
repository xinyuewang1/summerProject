from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Testtrip, Busstops
from busRoute.forms import routeForm
import requests
import json
import datetime
from datetime import date
import calendar

    

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
        context = {'weather': weather, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = routeForm(request.POST)
        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            return_time = form.cleaned_data['returnTime']
            depart_date = form.cleaned_data['departDate']
            return_date = form.cleaned_data['returnDate']

        weather = query_weather()
        args = {'form': form, 'source': source_address, 'destination': destination_address, 'depart_time': depart_time, 'return_time': return_time, 'depart_date': depart_date , 'return_date': return_date, 'weather': weather}
        return render(request, self.template_name, args)




class stopsView(generic.TemplateView):
    '''Class for stops.html page which renders the page, the form and the weather'''

    template_name = "busRoute/stops.html"
    context_object_name = 'weather'

    def get(self,request):
        form = routeForm()
        weather = query_weather()
        context = {'weather': weather, 'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = routeForm(request.POST)
        if form.is_valid():
            source_address = form.cleaned_data['source']
            destination_address = form.cleaned_data['destination']
            depart_time = form.cleaned_data['departTime']
            return_time = form.cleaned_data['returnTime']
            depart_date = form.cleaned_data['departDate']
            return_date = form.cleaned_data['returnDate']

        weather = query_weather()
        args = {'form': form, 'source': source_address, 'destination': destination_address, 'depart_time': depart_time, 'return_time': return_time, 'depart_date': depart_date , 'return_date': return_date, 'weather': weather}
        return render(request, self.template_name, args)



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








#have to add in weather to this bit, have to set the return to be disabled and add the extra styling and options for the form
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
                     'wind': float("{0:.2f}".format(3.6*(r['wind']['speed']))),
                     'icon': "http://openweathermap.org/img/w/" + str(r['weather'][0]['icon']) + ".png",
                     'day': calendar.day_name[my_date.weekday()],
                     'date': now.strftime("%d"),
                     'month': now.strftime("%B")}
    weatherInfo = json.dumps(weatherInfo)
    loaded_weather = json.loads(weatherInfo)

    return loaded_weather

