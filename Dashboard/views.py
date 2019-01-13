from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import re
import json
from . import queries as quer




# corrige les erreurs de type lors du passage d'une variable Javascript en Python
def varJavaToPython(x):
    if x == '':
        return None
    try:
        return int(x)
    except ValueError:
        return x







# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
#                                                                       #
#                       REQUETES PRINCIPALES                            #
#                                                                       #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #



""" recherche le/les id client(s) similaire(s) à 'id_input' """
# 'request': requete ajax contenant:
#    'id_input': chaine, la recherche de l'id client entrée par l'utilisateur
# ---> liste de chaines, les id similaires
@csrf_exempt
def sql_clt_search(request):
    message = request.POST.getlist('id_input[]')
    print('message',message)
    return HttpResponse(message[1])


    match = re.search('^([a-zA-Z])?(\d+)?$', id_input)
    if (not match or match.group(0) == ''):
        return []
    m_char = match.group(1)
    if m_char:
        m_char = m_char.upper()
    m_int = match.group(2)
    if m_int:
        m_int = "%%" + m_int + "%%"

    if (m_char != None and m_int != None):
        query = 'SELECT idMagasinVDSA, id FROM Client WHERE idMagasinVDSA = %s AND id LIKE %s'
        params = [m_char, m_int]
    elif (m_int != None):
        query = 'SELECT idMagasinVDSA, id FROM Client WHERE id LIKE %s'
        params = [m_int]
    else:
        query = 'SELECT idMagasinVDSA, id FROM Client WHERE idMagasinVDSA = %s'
        params = [m_char]

    table = quer.sql_execQuery(query, params, True)

    len_table = len(table)
    list = [None] * len_table
    for i in range(0,len_table):
        list[i] = table[i][0] + str(table[i][1])
    return list;



# ---> n-uplet de triplet de chaines, l'id, le nom et le prénom de tous les commercants
def sql_list_com():
    return quer.sql_execQuery('SELECT id, nom, prenom FROM Commercial ORDER BY nom', [], True)


# ---> n-uplet de couple, l'id et le nom de tous les magasins
def sql_list_mag():
    return quer.sql_execQuery('SELECT id, nom_magasin FROM MagasinVDSA ORDER BY nom_magasin', [], True)


# ---> n-uplet de couple, l'id et le nom de toutes les familles
def sql_list_fam():
    return quer.sql_execQuery('SELECT id, nom FROM Famille ORDER BY nom', [], True)


# ---> n-uplet de couple, l'id et le nom des sous-familles en fonction de l'id famille 'id_fam' dans la requete ajax GET 'request'
def sql_list_sous_fam(id_fam):
    query='SELECT id, nom FROM SousFamille WHERE idFamille = %s ORDER BY nom'
    params = [id_fam]
    return quer.sql_execQuery(query, params, True)




""" récupère toutes les données à afficher pour le graphique """
# 'request': requete ajax POST contenant en données:
#    'filter': liste de 5 chaines. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
#    'bool_ca': chaine, "True" si vrai, le graphique affichera les marges, sinon, CA
#
# ---> 'json_data': objet JSON contenant:
#
#         'graph_dates': tableau de 3 chaines, la date minimal, celle du milieu, et la date maximal affiché sur le graphique
#
#         'graph_data': tableau de 2 tableaux de 13 entiers, permettent de former le graphique. La 1ère liste contient
#                       les statistiques de l'année n-1, la 2eme de l'année n
#
#         'nb_clt', 'nb_newclt', 'ca_year', 'marge_year': tableaux de 3 entiers,
#               Les nombre de clients 'nb_clt', les nombre de nouveaux clients 'nb_newclt', les chiffre d'affaires 'ca_year'
#               et les marges 'marge_year' ont tous la même structure. Ils contiennent à chaque fois dans l'ordre la variation sur 2 ans,
#               la valeur pour l'année n-1 et pour l'année n en dernier
@csrf_exempt
def sql_get_table_data(request):
    filter = request.POST.getlist('filter[]')
    filter = [varJavaToPython(elt) for elt in filter]
    bool_ca = bool(request.POST['bool_ca'])

    print('\nsql_get_table_data')
    print('filter:',filter)
    print('bool_ca:',bool_ca, '\n')

    date_max = quer.getDateMax()
    (year_max, month_max, day_max) = (date_max.year, date_max.month, date_max.day)
    date_mid = quer.dtDate(year_max-1, month_max, day_max)
    date_min = quer.dtDate(year_max-2, month_max, day_max)
    graph_dates = (date_min.strftime('%d/%m/%Y'), date_mid.strftime('%d/%m/%Y'), date_max.strftime('%d/%m/%Y'))

    if bool_ca:
        graph_data = (
            quer.sql_caTableOfYear(year_max-2, date_max, filter),
            quer.sql_caTableOfYear(year_max-1, date_max, filter)
        )
    else:
        graph_data = (
            quer.sql_margeTableOfYear(year_max-2, date_max, filter),
            quer.sql_margeTableOfYear(year_max-1, date_max, filter)
        )

    nb_clt_before = quer.sql_nbCltOfYear(year_max-2, date_max, filter)
    nb_clt = quer.sql_nbCltOfYear(year_max-1, date_max, filter)
    nb_clt_var = quer.variation(nb_clt_before, nb_clt)

    nb_newclt_before = quer.sql_nbNewCltOfYear(year_max-2, date_max, filter)
    nb_newclt = quer.sql_nbNewCltOfYear(year_max-1, date_max, filter)
    nb_newclt_var = quer.variation(nb_newclt_before, nb_newclt)

    ca_year_before = quer.sql_caOfYear(year_max-2, date_max, filter)
    ca_year = quer.sql_caOfYear(year_max-1, date_max, filter)
    ca_year_var = quer.variation(ca_year_before, ca_year)

    marge_year_before = quer.sql_margeOfYear(year_max-2, date_max, filter)
    marge_year = quer.sql_margeOfYear(year_max-1, date_max, filter)
    marge_year_var = quer.variation(marge_year_before, marge_year)

    json_data = json.dumps({
        "graph_dates":graph_dates,
        "graph_data":graph_data,
        "nb_clt": [nb_clt_var, nb_clt_before, nb_clt],
        "nb_newclt": [ca_year_var, ca_year_before, ca_year],
        "ca_year": [ca_year_var, ca_year_before, ca_year],
        "marge_year": [marge_year_var, marge_year_before, marge_year]
    })

    return JsonResponse(json_data, status=200, safe=False)






""" obtient les donnée à affiché lorsque la souris passe sur un point du graphique """
# 'request': requete ajax POST contenant les données:
#    'x_table': entier, index de la liste qui a permis d'afficher le graphique (voir 'sql_getTableData').
#    'filter': liste de 5 chaines. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
#    'bool_ca': chaine, "True" si vrai, le graphique affichera les marges, sinon, CA
# ---> couple:
#         [0] triplet:
#              'graph_month_before': triplet de 1 entier et 2 dates, la valeur mensuel du CA ou marge et la date de début et de fin du mois pour l'année n-1
#              'graph_month': pareil que 'graph_month_before' mais pour l'année n
#              'graph_var_month': entier, variation entre la valeur du mois de l'année n-1 et de l'année n
#         [1] couple d'entiers:
#              'ca_per_clt': entier, chiffre d'affaire par client
#              'marge_month': entier, marge du mois
def sql_mouse_over(x_table, filter, bool_ca):
    date_max = quer.getDateMax()
    (year_max, month_max) = (date_max.year, date_max.month)
    month = ((x_table + month_max - 1) % 12) + 1

    if bool_ca:
        graph_month_before = quer.sql_caOfMonth(year_max-2, month, date_max, filter)
        graph_month = quer.sql_caOfMonth(year_max-1, month, date_max, filter)
    else:
        graph_month_before = quer.sql_margeOfMonth(year_max-2, month, date_max, filter)
        graph_month = quer.sql_margeOfMonth(year_max-1, month, date_max, filter)

    if (graph_month_before == None) or (graph_month == None):
        graph_var_month = None
    else:
        graph_var_month = graph_month[0] / graph_month_before[0] * 100 - 100

    ca_month = quer.sql_caOfMonth(year_max-1, month, date_max, filter)[0]
    nb_clt_month = quer.sql_nbCltOfMonth(year_max - 1, month, date_max, filter)
    if (ca_month == None) or (nb_clt_month == None):
        ca_per_clt = None
    else:
        ca_per_clt = ca_month / nb_clt_month

    marge_month = quer.sql_margeOfMonth(year_max-1, month, date_max, filter)[0]

    return (
        (graph_month_before, graph_month, graph_var_month),
        (ca_per_clt, marge_month)
    )






""" récupère les donnée pour l'affichage géolocalisé des marges ou du CA """
# 'request': requete ajax POST contenant les données:
#    'filter': liste de 5 chaines. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
#    'bool_ca': chaine, "True" si vrai, le graphique affichera les marges, sinon, CA
# ---> n-uplet de quadruplets contenant:
#           [0] entier, l'id de la localisation; [1] entier, le code postale; [2] chaine, le nom de la ville; [3] entier, la valeur de la marge ou CA
@csrf_exempt
def sql_get_geoloc_data(request):
    filter = request.POST.getlist('filter[]')
    filter = [varJavaToPython(elt) for elt in filter]
    bool_ca = bool(request.POST['bool_ca'])

    print('\nsql_get_geoloc_data')
    print('filter:',filter)
    print('bool_ca:',bool_ca, '\n')

    date_max = quer.getDateMax()
    year_max = date_max.year
    if bool_ca:
        data = quer.sql_geolocCA(year_max-1, date_max, filter)
    else:
        data = quer.sql_geolocMarge(year_max-1, date_max, filter)

    json_data = json.dumps(data)

    return JsonResponse(json_data, status=200, safe=False)






# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
#                                                                       #
#                          DASHBOARD                                    #
#                                                                       #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #

# affiche la page HTML du tableau de bord
def dashboard(request):



    return render(request,"dashboard/dashboard.html")
