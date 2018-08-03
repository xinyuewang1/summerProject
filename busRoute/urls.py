from django.conf.urls import url
from django.urls import path
from . import views
from .views import Est39A
from .models import Testtrip
from .views import Est39A #, AnnEst39A

urlpatterns = [


    #URLs for the main pages
    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^planner', views.plannerView.as_view(), name='planner'),

    url(r'^result', views.resultView.as_view(), name='result'),

    url(r'^tourism', views.tourismView.as_view(), name='tourism'),


    url(r'dublinBusInfo', views.DublinBusInfo, name = 'DublinBusInfo'),

    #This URL is used for Autocomplete Information for the form
    url(r'^RouteInfo', views.GenBusData, name='RouteInfo'),

    # This URL is used for Autocomplete Information for the Route Search Option
    url(r'^dublinBusRoutes', views.DublinBusRoutes, name='dublinBusRoutes'),

     #This URL passes the route to the get_route_data function in views.py
    path('details/<slug:route>/', views.get_route_data, name='detail'),

    path('busNum/<slug:bus>/', views.getRoute, name='busNum'),
 

    #Pickle
    url(r'Ett39A', Est39A, name="Ett39A"),

    #url(r'Ann39A', AnnEst39A, name='Ann39A'),

]