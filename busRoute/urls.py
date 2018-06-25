from django.conf.urls import url
from django.urls import path
from . import views
from .models import Testtrip

urlpatterns = [

    url(r'^index', views.index, name='index'),

    url(r'^stop', views.stops, name='stops'),

    url(r'^tour', views.tourism, name='tourism'),
    
    # url(r'^(?P<busroutenum>[0-9]+)/$', views.detail, name='detail'),

    # url(r'^(?P<busroutenum>[0-9]+)/$', views.query_weather, name='detail'),

]

