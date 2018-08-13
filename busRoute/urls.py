from django.conf.urls import url
from django.urls import path
from . import views

from .views import Est39A
from busRoute.views import GenBusData, bikes_query, DublinBus
from .models import Testtrip
from .views import Est39A #, AnnEst39A

#Error Pages
handler400 = 'views.handler400'
handler401 = 'views.handler401'
handler403 = 'views.handler403'
handler404 = 'views.handler404'
handler408 = 'views.handler408'
handler410 = 'views.handler410'
handler418 = 'views.handler418'
handler421 = 'views.handler421'
handler424 = 'views.handler424'
handler426 = 'views.handler426'
handler429 = 'views.handler429'
handler500 = 'views.handler500'
handler501 = 'views.handler501'
handler502 = 'views.handler502'
handler503 = 'views.handler503'
handler504 = 'views.handler504'
handler507 = 'views.handler507'
handler508 = 'views.handler508'
handler511 = 'views.handler511'

urlpatterns = [


    #URLs for the main pages

    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^result', views.resultView.as_view(), name='result'),

    url(r'^tourism', views.tourismView.as_view(), name='tourism'),

    #These URL's contain the data necessary for Autocomplete functions. 
    url(r'^RouteInfo', views.GenBusData, name='RouteInfo'),

    url(r'^problem', views.problemView.as_view(), name='problem'),

    url(r'^dublinBusRoutes', views.routeDirectionServices, name='dublinBusRoutes'),
    url(r'^dublinBusInfo', views.DublinBusInfo, name = 'DublinBusInfo'),

    #contains the information for the bikes data 
    
    url(r'^dublinBikeInfo', views.bikes_query, name='dublinBikeInfo'),

    url(r'dublinBusInfo', views.DublinBusInfo, name = 'DublinBusInfo'),

    #data rendered here is used for the suggested stops near the user selections. 
    url(r'^nearestBus/(-?\d+(?:\.\d+)?)/(-?\d+(?:\.\d+)?)', views.stopNearMe, name='nearestBus'),

    #This URL passes the route to the get_route_data function in views.py

    #?P<route>[\w\ ]
    url(r'^details/(?P<route>[\w\ ]+)', views.get_route_data, name='detail'),

    path('busNum/<slug:bus>/', views.getRoute, name='busNum'),

    # url(r'^markerInformation/(?P<name>[\w,\ ]+)/(?P<num>[\w,\ ]+)', views.markerInformation, name='busNum'),

    #Pickle
    url(r'Ett39A', Est39A, name="Ett39A"),

    #url(r'Ann39A', AnnEst39A, name='Ann39A'),

    url(r'', views.plannerView.as_view(), name='planner'),

]