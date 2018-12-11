

from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    #/CompteUtilisateur/connexion
    url(r'^connexion$',views.connexion),
    #/CompteUtilisateur/nvMDP
    url(r'^nvMDP$',views.nvMDP),
]
