from __future__ import absolute_import

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


    return render(request,"Geolocalisation/geolocalisation.html",
    { "representants" : representants, "magasins":magasins, "familles" : familles} )


# ---> n-uplet de couple, l'id et le nom des sous-familles en fonction de l'id famille 'id_fam' dans la requete ajax GET 'request'
@csrf_exempt
def sql_list_sous_fam(request):
# i faut lever l'exceptin ValueError dans le cas ou la valeur vaut "null" quand il selectionne toutes les famille
    id_famille = int(request.POST['famille'])
    print("famille:",id_famille)

    data = query_view.sql_list_sous_fam(id_famille)
    print("sous famille:",data)
    json_data = json.dumps(data)
    return JsonResponse(json_data, status=200, safe=False)
