from django.conf.urls import url
from django.urls import path
from . import views
from .models import Testtrip

urlpatterns = [

    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^stop', views.stopsView.as_view(), name='stops'),

    url(r'^tour', views.tourism, name='tourism'),

     url(r'^routes', views.routes, name='tourism'),

    # url(r'^stop', views.stops, name='stops'),

    # url(r'^index', views.index, name='index'),
    
    url(r'^(?P<busroutenum>[0-9]+)/$', views.timeGenerator, name='detail'),

    url(r'^api/getSource/', views.getSource, name='getSource'),

    url(r'^api/getSource/', views.getSource, name='getSource'),

    url(r'^api/getDesintation/', views.getDestination, name='getDestination'),

    url(r'^api/getAddressSource/', views.getAddressSource, name='getSourceAddress'),

    url(r'^api/getAddressDestination/', views.getAddressDestination, name='getDestinationAddress'),

]

