

from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.connexion),
    url(r'^connexion$',views.connexion),
    url(r'^nvMDP$',views.nvMDP),
]
