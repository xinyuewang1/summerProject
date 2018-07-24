from django.conf.urls import url
from django.urls import path
from . import views
from .views import Est39A
from .models import Testtrip

urlpatterns = [

    url(r'^index', views.homeView.as_view(), name='index'),

    url(r'^planner', views.plannerView.as_view(), name='planner'),

    url(r'^routes', views.routesView.as_view(), name='routes'),

    url(r'^result', views.resultView.as_view(), name='result'),

    url(r'^tour', views.tourism, name='tourism'),

 
    url(r'^(?P<busroutenum>[0-9]+)/$', views.timeGenerator, name='detail'),

    url(r'^api/getRoutes/', views.getRoutes, name='getRoutes'),

    url(r'^api/getSource/', views.getSource, name='getSource'),

    url(r'^api/getDesintation/', views.getDestination, name='getDestination'),

    url(r'^api/getAddressSource/', views.getAddressSource, name='getSourceAddress'),

    url(r'^api/getAddressDestination/', views.getAddressDestination, name='getDestinationAddress'),

    #Pickle
    url(r'Ett39A', Est39A, name="Ett39A"),

]

