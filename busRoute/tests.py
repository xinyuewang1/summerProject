from django.test import TestCase
from django.test import Client
from django.conf import settings
from busRoute.views import *
import unittest
import requests
import datetime

# Create your tests here.
class TestViews(unittest.TestCase):

    def test_DublinBus_Response(self):

        bus = DublinBus()
        self.assertTrue(bus)

    def test_stopNearMe_Response(self):

        c = Client()
        response = c.get('/nearestBus')
        x = response.status_code
        self.assertTrue(200)

    def test_query_weather_Response(self):

        weather = query_weather()
        self.assertTrue(weather)
      
    def test_bikes_query_Response(self):

        c = Client()
        response = c.get('/dublinBikeInfo')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_DublinBusInfo_Response(self):

        c = Client()
        response = c.get('/dublinBusInfo')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_get_route_data_Response(self):

        c = Client()
        response = c.get('/details/39A/')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_GenBusData_Response(self):

        c = Client()
        response = c.get('/RouteInfo')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_DublinBusRoutes_Response(self):

        c = Client()
        response = c.get('/dublinBusRoutes')
        x = response.status_code
        self.assertTrue(x == 200)
    
    def test_query_rain_weather_Response(self):

        date = datetime.datetime.now().strftime('%m/%d/%Y')
        time = datetime.datetime.now().strftime('%H:%M')
        rain, temp = query_rain_weather(time, date)
        self.assertTrue(rain, temp)

    def test_googDir_Response(self):

        origin = '53.381131,-6.592682'
        dest = '53.298665 -6.302196'
        date = datetime.datetime.now().strftime('%m/%d/%Y')
        time = datetime.datetime.now().strftime('%H:%M')
        directions = googDir(origin, dest, date, time)
        self.assertFalse(directions)

    def test_findLatLong_Response(self):

        loc = findLatLong('768')
        self.assertFalse(loc)

    def test_getRoute(self):

        c = Client()
        response = c.get('/busNum/39A/')
        x = response.status_code
        self.assertTrue(x == 200)

    def test_Est39A_response(self):

        route = '39A'
        source = '768'
        dest = '769'
        dateStr = datetime.datetime.now().strftime('%m/%d/%Y')
        timeStr = datetime.datetime.now().strftime('%H:%M')
        precipitation, temp = query_rain_weather(timeStr, dateStr)
        weekday = '3'
        est = Est39A(route, source, dest, precipitation, temp, timeStr, weekday, dateStr)
        
    
        
if __name__ == '__main__':
    unittest.main()

