from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    #render(request,template_name,variables)
    #return render(request,"connexion.html")
    return HttpResponse("index du serveur")
