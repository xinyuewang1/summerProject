from django.conf.urls import url
from django.urls import path
from . import views
from .models import Testtrip

urlpatterns = [

    url(r'^index', views.index, name='index'),

    url(r'^stop', views.stops, name='stops'),

    url(r'^tour', views.tourism, name='tourism'),

     url(r'^routes', views.routes, name='tourism'),
    
    # url(r'^(?P<busroutenum>[0-9]+)/$', views.detail, name='detail'),

    # url(r'^(?P<busroutenum>[0-9]+)/$', views.query_weather, name='detail'),

    url(r'^api/getSource/', views.getSource, name='getSource'),

    url(r'^api/getDesintation/', views.getDestination, name='getDestination'),

    url(r'^api/getAddressSource/', views.getAddressSource, name='getSourceAddress'),

    url(r'^api/getAddressDestination/', views.getAddressDestination, name='getDestinationAddress'),

]

