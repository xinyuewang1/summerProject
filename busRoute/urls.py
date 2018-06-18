from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^stop', views.stops, name='stops'),
    url(r'^tour', views.tourism, name='tourism'),
]