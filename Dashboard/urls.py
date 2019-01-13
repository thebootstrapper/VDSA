
from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    #/Dashboard/
    url(r'^$',views.dashboard,name="dashboard"),
    url(r'^sql_clt_search/$',views.sql_clt_search,name="sql_clt_search"),
    url(r'^sql_get_table_data/$',views.sql_get_table_data,name="sql_get_table_data"),
    url(r'^sql_get_geoloc_data/$',views.sql_get_geoloc_data,name="sql_get_geoloc_data"),
]
