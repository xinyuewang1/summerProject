from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^(?P<chosen_time>[0-9]+)/$', views.timeGenerator, name='detail'),
    #Note: this regex needs to be made more effecient.It will stop at certain time intervals; 
    url(r'^(?P<chosen_time>[0-2][0-3]:[0-5][0-9]+)/$', views.timeGenerator, name='detail'),

    url(r'^index', views.index, name='index'),

    url(r'^stop', views.stops, name='stops'),

    url(r'^tour', views.tourism, name='tourism'),
    
]

