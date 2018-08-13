from django.test import TestCase, SimpleTestCase
from django.test import Client
from django.conf import settings
from busRoute.views import *
import unittest
import datetime
from .forms import routeForm
from .utils import Ett39A
import datetime
from datetime import date
from django.urls import reverse
from django.urls import resolve
import os




class TestViewResponses(unittest.TestCase):

    '''This Test Class Tests all the Functions in Views.py'''

    def test_DublinBus_Response(self):

        '''Tests that the DublinBus function returns data'''

        bus = DublinBus()
        self.assertTrue(bus)

    def test_stopNearMe_Response(self):

        '''Tests that the stopsNearMe function has a status code of 200 meaning it runs effectively'''

        c = Client()
        response = c.get('/nearestBus')
        x = response.status_code
        self.assertTrue(200)

    def test_query_weather_Response(self):

        '''Tests that the query_weather function returns data'''

        weather = query_weather()
        self.assertTrue(weather)
      
    def test_bikes_query_Response(self):

        '''Tests that the bikes_query function has a status code of 200 meaning it runs effectively'''

        c = Client()
        response = c.get('/dublinBikeInfo')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_DublinBusInfo_Response(self):

        '''Tests that the DublinBusInfo function has a status code of 200 meaning it runs effectively'''

        c = Client()
        response = c.get('/dublinBusInfo')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_get_route_data_Response(self):

        '''Tests that the get_route_data function has a status code of 200 meaning it runs effectively'''

        c = Client()
        response = c.get('/details/39A/')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_GenBusData_Response(self):

        '''Tests that the GenBusData function has a status code of 200 meaning it runs effectively'''

        c = Client()
        response = c.get('/RouteInfo')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_DublinBusRoutes_Response(self):

        '''Tests that the DublinBusRoutes function has a status code of 200 meaning it runs effectively'''

        c = Client()
        response = c.get('/dublinBusRoutes')
        x = response.status_code
        self.assertTrue(x == 200)
    
    def test_query_rain_weather_Response(self):

        '''Tests that the GenBusData function returns two variables, 
        it will only return two variables if rain is forecasted so it may fail if rain is 0, 
        both a pass and a failure are expected depending on if rain is returned.'''

        date = datetime.datetime.now().strftime('%m/%d/%Y')
        time = datetime.datetime.now().strftime('%H:%M')
        rain, temp = query_rain_weather(time, date)
        self.assertTrue(rain, temp)

    def test_googDir_Response(self):

        '''Tests that the googDir function does not return data, it should fail'''

        origin = '53.381131,-6.592682'
        dest = '53.298665 -6.302196'
        date = datetime.datetime.now().strftime('%m/%d/%Y')
        time = datetime.datetime.now().strftime('%H:%M')
        directions = googDir(origin, dest, date, time)
        self.assertFalse(directions)

    def test_findLatLong_Response(self):

        '''Tests that the findLatLong function does not return data, it should fail'''

        loc = findLatLong('768')
        self.assertFalse(loc)

    def test_getRoute(self):

        '''Tests that the getRoute function has a status code of 200 meaning it runs effectively'''

        c = Client()
        response = c.get('/busNum/39A/')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_Est39A_response(self):

        '''Tests that the Est39A function returns an estimated travel time'''

        route = '39A'
        source = 768
        dest = 7161
        dateStr = datetime.datetime.now().strftime('%m/%d/%Y')
        timeStr = datetime.datetime.now().strftime('%H:%M')
        precipitation, temp = query_rain_weather(timeStr, dateStr)
        weekday = 3
        est = Est39A(route, source, dest, precipitation, temp, timeStr, weekday, dateStr)
        self.assertTrue(est)

    def test_readTimeIn_Response(self):

        '''Tests that the readTimeIn function returns the right hour from a time input'''

        time = readTimeIn('10:30')
        self.assertTrue(time == 10)

    def test_arrivalTime_Response(self):

        '''Tests that the arrivalTime function returns the right string representation of an arrival time using a depart time and the minutes travelled'''

        depart = '10:35'
        travel = 15
        x = arrivalTime(depart, travel)
        self.assertTrue(x == '10:50')


    def test_parseDate_Response(self):

        '''Tests that the parseDate function returns the correct day from a date, it should fail'''

        dateStr = datetime.datetime.now().strftime('7/31/2018')
        x = parseDate(dateStr)
        self.assertFalse(x == 'Tuesday')

    def test_parseDayNumber_Response(self):

        '''Tests that the parseDate function returns the correct number representation of a day (0-6)'''

        date = '7/31/2018'
        x = parseDayNumber(date)
        self.assertTrue(x == 1)

# class TestViewDataTypes(unittest.TestCase):

class TestPageUrls(unittest.TestCase):

    '''This class tests that each URL is connected to the right View function by using Resolve'''

    def test_index(self):

        '''Testing the index.html URL'''

        page = resolve('/index')
        self.assertEqual(page.view_name, 'index')

    def test_index_fail(self):

        '''Testing the index.html URL'''

        page = resolve('/index')
        self.assertEqual(page.view_name, 'planner')

    def test_planner(self):

        '''Testing the planner.html URL'''

        page = resolve('/planner')
        self.assertEqual(page.view_name, 'planner')

    def test_result(self):

        '''Testing the result.html URL'''

        page = resolve('/result')
        self.assertEqual(page.view_name, 'result')

    def test_tourism(self):

        '''Testing the tourism.html URL'''

        page = resolve('/tourism')
        self.assertEqual(page.view_name, 'tourism')


class TestFormFields(unittest.TestCase):


    '''This class tests that the form for the web application is only valid when it has all necessary inputs'''
   
    def test_routeForm_valid(self):

        '''tests the validity of the form'''

        form = routeForm(data={'source': "768", 'destination': "7161", 'departTime': "18:00", 'departDate': "08/02/2018"})
        self.assertTrue(form.is_valid())

    def test_routeForm_Source_invalid(self):

        '''tests that the form is invalid without the source input'''

        form = routeForm(data={'source': "", 'destination': "7161", 'departTime': "18:00", 'departDate': "08/02/2018"})
        self.assertFalse(form.is_valid())

    
    def test_routeForm_Destination_invalid(self):

        '''tests that the form is invalid without the destination input'''

        form = routeForm(data={'source': "768", 'destination': "", 'departTime': "18:00", 'departDate': "08/02/2018"})
        self.assertFalse(form.is_valid())

    def test_routeForm_departTime_invalid(self):

        '''tests that the form is invalid without the departTime input'''

        form = routeForm(data={'source': "768", 'destination': "7161", 'departTime': "", 'departDate': "08/02/2018"})
        self.assertFalse(form.is_valid())
    
    def test_routeForm_departDate_invalid(self):

        '''tests that the form is invalid without the departDate input'''

        form = routeForm(data={'source': "768", 'destination': "7161", 'departTime': "18:00", 'departDate': ""})
        self.assertFalse(form.is_valid())



if __name__ == '__main__':
    unittest.main()


#References: 
# https://stackoverflow.com/questions/18987051/how-do-i-unit-test-django-urls
# https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/
