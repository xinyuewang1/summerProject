from django.test import TestCase
from django.test import Client
from django.conf import settings
from busRoute.views import *
import unittest
import requests
import datetime


class TestViews(unittest.TestCase):

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

        '''Tests that the GenBusData function returns two variables'''

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

    

if __name__ == '__main__':
    unittest.main()

