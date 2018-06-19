from django.conf.urls import url
from . import views

urlpatterns = [   
    #Note: this regex needs to be made more effecient.It will stop at certain time intervals; 
    #Note: the best option is to use PATH. Will figure out how to link Path to months, time etc. Regex is time consuming.
    
    url(r'^(?P<chosen_time>[0-2][0-9]:[0-5][0-9]+)/$', views.timeGenerator, name='detail'),

    url(r'^return/(?P<returnTime>[0-2][0-9]:[0-5][0-9]+)/$', views.returntimeGenerator, name='return'),

    url(r'^month/(?P<month>\d{1,2}\/\d{1,2}\/\d{4})/$', views.deptMonth, name='month'),

    url(r'^return/month/(?P<returnmonth>\d{1,2}\/\d{1,2}\/\d{4})/$', views.retMonth, name='month'),

    url(r'^index', views.index, name='index'),

    url(r'^stop', views.stops, name='stops'),

    url(r'^tour', views.tourism, name='tourism'),

]

