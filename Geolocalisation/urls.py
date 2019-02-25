from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    #/Geolocalisation/
    url(r'^$',views.geolocalisation,name="geolocalisation"),
    url(r'^sql_list_sous_fam/$',views.sql_list_sous_fam,name="sql_list_sous_fam"),
]
