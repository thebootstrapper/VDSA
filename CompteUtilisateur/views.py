from django.shortcuts import render
from django.http import HttpResponse


def connexion(request):
    #render(request,template_name,variables)
    return render(request,"CompteUtilisateur/connexion.html")
#    return HttpResponse("connexion")




def nvMDP(request):
    return render(request,"CompteUtilisateur/nvMDP.html")
