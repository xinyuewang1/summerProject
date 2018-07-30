from django.conf.urls import url
from django.urls import path
from . import views
from .views import Est39A
from .models import Testtrip
from .views import Est39A #, AnnEst39A

urlpatterns = [

<<<<<<< HEAD
    #URLs for the main pages
    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^planner', views.plannerView.as_view(), name='planner'),

    url(r'^result', views.resultView.as_view(), name='result'),

    url(r'^tourism', views.tourismView.as_view(), name='tourism'),



    #This URL is used for Autocomplete Information for the form
    url(r'^RouteInfo', views.GenBusData, name='RouteInfo'),

    # This URL is used for Autocomplete Information for the Route Search Option
    url(r'^dublinBusRoutes', views.DublinBusRoutes, name='dublinBusRoutes'),

     #This URL passes the route to the get_route_data function in views.py
    path('details/<slug:route>/', views.get_route_data, name='detail'),

    path('busNum/<slug:bus>/', views.getRoute, name='busNum'),
 
=======
    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^stop', views.stopsView.as_view(), name='stops'),

    url(r'^routes', views.routesView.as_view(), name='routes'),

    url(r'^tour', views.tourism, name='tourism'),

    url(r'^test', views.test, name='tourism'),
    
 
    url(r'^(?P<busroutenum>[0-9]+)/$', views.timeGenerator, name='detail'),

    url(r'^api/getRoutes/', views.getRoutes, name='getRoutes'),

    url(r'^api/getSource/', views.getSource, name='getSource'),

    url(r'^api/getDesintation/', views.getDestination, name='getDestination'),

    url(r'^api/getAddressSource/', views.getAddressSource, name='getSourceAddress'),

    url(r'^api/getAddressDestination/', views.getAddressDestination, name='getDestinationAddress'),
>>>>>>> WangBranch
    #Pickle
    url(r'Ett39A', Est39A, name="Ett39A"),

    #url(r'Ann39A', AnnEst39A, name='Ann39A'),

]