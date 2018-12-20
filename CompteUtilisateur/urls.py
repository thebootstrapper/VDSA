

from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    #/quand l'url est "CompteUtilisateur/connexion" on appelle la fonction views.connexion qui chargera le template connexion.html
    url(r'^connexion$',views.connexion),
    #/CompteUtilisateur/nvMDP
    url(r'^nvMDP$',views.nvMDP),
]
