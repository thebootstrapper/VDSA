from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    #/Geolocalisation/
    url(r'^$',views.geolocalisation,name="geolocalisation"),
]
