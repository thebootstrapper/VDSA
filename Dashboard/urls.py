
from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    #/Dashboard/
    url(r'^$',views.dashboard,name="dashboard"),
]
