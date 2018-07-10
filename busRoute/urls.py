from django.conf.urls import url
from django.urls import path
from . import views
from .models import Testtrip

urlpatterns = [

    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^stop', views.stopsView.as_view(), name='stops'),

    url(r'^tour', views.tourism, name='tourism'),
    
    url(r'^(?P<busroutenum>[0-9]+)/$', views.timeGenerator, name='detail'),

    #Autocomplete for Stop_id 
    url(r'^api/getSource/', views.getSource, name='getSource'),

]

