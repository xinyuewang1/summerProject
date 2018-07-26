from django.conf.urls import url
from django.urls import path
from . import views

from .views import Est39A
from busRoute.views import GenBusData
from .models import Testtrip

urlpatterns = [


    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^planner', views.plannerView.as_view(), name='planner'),

    url(r'^routes', views.routesView.as_view(), name='routes'),

    url(r'^result', views.resultView.as_view(), name='result'),

    url(r'^tour', views.tourism, name='tourism'),

    #This URL is used for Autocomplete Information for the form

    url(r'^RouteInfo', views.GenBusData, name='RouteInfo'),



    url(r'^nearestBus', views.stopNearMe, name='nearestBus'),


    # This URL is used for Autocomplete Information for the Route Search Option
    url(r'^dublinBusRoutes', views.DublinBusRoutes, name='dublinBusRoutes'),

     #This URL passes the route to the get_route_data function in views.py

    path('details/<slug:route>/', views.get_route_data, name='detail'),

    url(r'^(?P<busroutenum>[0-9]+)/$', views.timeGenerator, name='detail'),

    #Pickle
    url(r'Ett39A', Est39A, name="Ett39A"),

]

