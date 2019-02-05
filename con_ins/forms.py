from django import forms
from .choices import *

class Connexion_form(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class Inscription_form(forms.Form):
    nom = forms.CharField()
    prenom = forms.CharField()
    email = forms.EmailField()
    statut = forms.ChoiceField(choices = CHOIX_STATUT)
    magasin = forms.CharField()
