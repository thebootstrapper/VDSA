
from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    #/Backoffice
   url(r'^$',views.lecture_fichier,name="lecture_fichier"),
]
