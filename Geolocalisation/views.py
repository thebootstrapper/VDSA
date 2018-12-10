from django.shortcuts import render
from django.http import HttpResponse


def geolocalisation(request):
    return render(request,"Geolocalisation/geolocalisation.html")
