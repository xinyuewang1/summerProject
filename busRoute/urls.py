from django.conf.urls import url
from django.urls import path
from . import views

from .views import Est39A
from busRoute.views import GenBusData, bikes_query, DublinBus
from .models import Testtrip
from .views import Est39A #, AnnEst39A

urlpatterns = [


    #URLs for the main pages
    url(r'', views.homeView.as_view(), name='index'),
    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^planner', views.plannerView.as_view(), name='planner'),

    url(r'^result', views.resultView.as_view(), name='result'),

    url(r'^tourism', views.tourismView.as_view(), name='tourism'),

    #These URL's contain the data necessary for Autocomplete functions. 
    url(r'^RouteInfo', views.GenBusData, name='RouteInfo'),

    url(r'^dublinBusRoutes', views.routeDirectionServices, name='dublinBusRoutes'),

    #contains the information for the bikes data 
    url(r'^dublinBikeInfo', views.bikes_query, name='dublinBikeInfo'),

    url(r'dublinBusInfo', views.DublinBusInfo, name = 'DublinBusInfo'),

    #data rendered here is used for the suggested stops near the user selections. 
    url(r'^nearestBus/(-?\d+(?:\.\d+)?)/(-?\d+(?:\.\d+)?)', views.stopNearMe, name='nearestBus'),

    #This URL passes the route to the get_route_data function in views.py

    #?P<route>[\w\ ]
    url(r'^details/(?P<route>[\w\ ]+)', views.get_route_data, name='detail'),

    path('busNum/<slug:bus>/', views.getRoute, name='busNum'),
 

    #Pickle
    url(r'Ett39A', Est39A, name="Ett39A"),

    #url(r'Ann39A', AnnEst39A, name='Ann39A'),

]