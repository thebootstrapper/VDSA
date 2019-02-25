from __future__ import absolute_import

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Backoffice.models import Session_utilisateur, Commercial, Magasinvdsa, Admin

import json

import Dashboard
from Dashboard import views as query_view


def geolocalisation(request):

    # ---> n-uplet de triplet de chaines, l'id, le nom et le prénom de tous les commercants
    representants=query_view.sql_list_com();
    # ---> n-uplet de couple, l'id et le nom de tous les magasins
    magasins= query_view.sql_list_mag();

    # ---> n-uplet de couple, l'id et le nom de toutes les familles
    familles  = query_view.sql_list_fam();


    email_s = Session_utilisateur.objects.all().last().email_s
    statut = Session_utilisateur.objects.all().last().statut_s

    if statut == "commercial":
        id = Commercial.objects.get(email = email_s).id
        nom = Commercial.objects.get(email = email_s).nom
        prenom = Commercial.objects.get(email = email_s).prenom
    elif statut == "directeur":
        id = Magasinvdsa.objects.get(email_directeur = email_s).id
        nom = Magasinvdsa.objects.get(email = email_s).nom_directeur
        prenom = Magasinvdsa.objects.get(email = email_s).prenom_directeur
    elif statut == "administrateur":
       id = Admin.objects.get(email = email_s).id
       nom = Admin.objects.get(email = email_s).nom
       prenom = Admin.objects.get(email = email_s).prenom



    return render(request,"Geolocalisation/geolocalisation.html",{
        "representants" : representants,
        "magasins": magasins,
        "familles" : familles,
        "id": id,
        "statut": statut,
        "email_s":email_s,
        "nom":nom,
        "prenom":prenom
    })





# ---> n-uplet de couple, l'id et le nom des sous-familles en fonction de l'id famille 'id_fam' dans la requete ajax GET 'request'
@csrf_exempt
def sql_list_sous_fam(request):
# i faut lever l'exceptin ValueError dans le cas ou la valeur vaut "null" quand il selectionne toutes les famille
    id_famille = int(request.POST['fid_fam'])
    print("id famille envoyer par django:",id_famille)

    jsonResponse = query_view.sql_list_sous_fam(request)
    return jsonResponse
