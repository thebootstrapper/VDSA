from datetime import date as dtDate
from calendar import monthrange
from django.db import connection
from decimal import Decimal






# Variation entre 2 décimales en pourcent
def variation(x, y):
    if x:
        return ((y - x) / abs(x) * 100)
    elif y:
        return None
    else:
        return 0


# Convertir un objet décimal en float
def decimalToFloat(x):
    try:
        return float(x)
    except TypeError:
        return None







# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
#                                                                       #
#                         OUTILS REQUETES                               #
#                                                                       #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #



""" obtenir la date maximale affichée sur graphique """
# Dans l'exemple de graphique du sujet, il s'agit du 5 septembre 2018
# ---> objet date, la date maximale
def getDateMax():
    # Le mois et le jour de la date maximal
    month_max = 9
    day_max = 5

    date_current = dtDate.today()
    year_current = date_current.year
    date_max = dtDate(year_current,month_max,day_max)
    if date_current < date_max:
        date_max = date_max.replace(year=year_current-1)
    return date_max



""" Calculer la marge selon un tableau montant marge """
# table: tableau de tableaux de décimales, dans l'ordre, montant puis marge
# ---> décimal, marge en pourcent
def calcMarge(table):
    if (not table):
        return None
    sumP, sum = 0, 0
    len_table = len(table)
    for i in range(0, len_table):
        montant = table[i][0]
        marge = table[i][1]
        sum += montant - (abs(montant) * marge) / 100
        sumP += montant

    if (sumP == 0 and sum == 0):
        return 0
    elif (sumP == 0):
        return None
    else:
        marge = (sumP - sum) / abs(sumP) * 100
        return marge



def sql_execQuery(query, params, bool_fetchall):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if bool_fetchall == True:
            sql_response = cursor.fetchall()
        else:
            sql_response = cursor.fetchone()
    return sql_response;







# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
#                                                                       #
#                       REQUETES GRAPHIQUE ANNUELLE                     #
#                                                                       #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #



""" ajouter le filtre selon l'id client, commercial et magasin à la requete SQL"""
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# 'query': chaine, contient le début de la requete SQL terminant par un WHERE ...
# 'params': liste contenant les paramètres à executer avec 'query'
# ---> doublet: 'query': chaine, requête SQL complété avec le filtre 'filter'
#               'params': liste contenant les paramètres à executer avec 'query'
def sql_addFilter(filter, query, params):
    id_clt = filter[0]
    id_com = filter[1]
    id_mag = filter[2]
    id_sfam = filter[3]
    id_fam = filter[4]
    if (id_clt):
        query += ' AND f.idClient = %s'
        params.append(id_clt)
    if (id_com):
        query += ' AND f.idCommercial = %s'
        params.append(id_com)
    if (id_mag):
        query += ' AND f.idMagasinVDSA = %s'
        params.append(id_mag)
    if (id_sfam):
        query += ' AND f.idSousFamille = %s'
        params.append(id_sfam)
    if (id_fam):
        query += ' AND f.idSousFamille IN ( SELECT id FROM SousFamille WHERE idFamille = %s )'
        params.append(id_fam)
    return (query, params)





""" obtenir le premier et le dernier jour d'un mois en fonction de 'date_max' """
# 'year', 'month': entiers, année et mois désirés
# 'date_max': objet date, date maximal
# ---> doublet de 2 objets date correspondant au premier et au dernier jour. (None, None) si hors du graph
def sql_getRangeOfMonth(year, month, date_max):
    date_min = date_max.replace(year = date_max.year - 2)
    day_end_month = monthrange(year,month)[1]

    # Date hors du graphique
    if dtDate(year, month, day_end_month) < date_min or dtDate(year, month, 1) > date_max:
        return (None, None)

    month_max = date_max.month
    year_max = date_max.year

    # extreme droite du graphique, courbe n
    if month == month_max and year == year_max:
        return (dtDate(year, month, 1), date_max)

    # extreme gauche du graphique, courbe n-1
    elif month == month_max and year == year_max - 2:
        return (date_min, dtDate(year, month, day_end_month))

    else:
        return (dtDate(year, month, 1), dtDate(year, month, day_end_month))




""" obtenir la marge d'un mois """
# 'year', 'month': entiers, année et mois désirés
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> triplet: 'marge_of_month': décimal, infinie ou None, marge du mois. None si aucune donnée ou hors du graphique
#               'date_begin_month': objet date, date du début du mois. None si hors du graphique
#               'date_end_month': objet date, date de la fin du mois. None si hors du graphique
def sql_margeOfMonth(year, month, date_max, filter):
    (date_begin_month, date_end_month) = sql_getRangeOfMonth(year, month, date_max)
    if (not date_begin_month):
        return (None, None, None)

    query = "SELECT f.montant, f.marge FROM Facture f WHERE f.date >= %s AND f.date <= %s"
    params = [date_begin_month, date_end_month]
    (query, params) = sql_addFilter(filter, query, params)
    marge_of_month = calcMarge(sql_execQuery(query, params, True))
    return ( decimalToFloat(marge_of_month), date_begin_month, date_end_month )




""" obtenir un tableau des marges à afficher sur le graphique dans l'ordre pour une année """
# 'year': entier, année désiré. 2017 pour 2017-2018
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> tableau de 13 décimales: Marges par mois en commencant et finissant par Septembre (voir exemple sujet)
def sql_margeTableOfYear(year, date_max, filter):
    table = [None] * 13
    for i in range(0, 13):
        month = date_max.month + i
        table[i] = sql_margeOfMonth( year + (month > 12), ((month-1) % 12) + 1, date_max, filter )[0]
    return table




""" obtenir la somme du chiffre d'affaire d'un mois """
# 'year', 'month': entiers, année et mois désirés
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> triplet: 'sum_ca': décimal, somme du CA du mois. None si aucune donnée ou hors du graphique
#               'date_begin_month': objet date, date du début du mois. None si hors du graphique
#               'date_end_month': objet date, date de la fin du mois. None si hors du graphique
def sql_caOfMonth(year, month, date_max, filter):
    (date_begin_month, date_end_month)=sql_getRangeOfMonth(year, month, date_max)
    if (not date_begin_month):
        return (None, None, None)

    query='SELECT SUM(f.montant) FROM Facture f WHERE f.date >= %s AND f.date <= %s'
    params = [date_begin_month, date_end_month]
    (query, params) = sql_addFilter(filter, query, params)
    sum_ca = sql_execQuery(query, params, False)[0]

    return ( decimalToFloat(sum_ca), date_begin_month, date_end_month )




""" obtenir un tableau des chiffre d'affaire à afficher sur le graphique dans l'ordre pour une année """
# 'year': entier, année désiré. 2017 pour 2017-2018
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> tableau de 13 décimales: CA par mois en commencant et finissant par Septembre (voir exemple sujet)
def sql_caTableOfYear(year, date_max, filter):
    table = [None] * 13
    for i in range(0, 13):
        month = date_max.month + i
        table[i] = sql_caOfMonth(year + (month > 12), ((month-1) % 12) + 1, date_max, filter)[0]
    return table






# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
#                                                                       #
#                    REQUETES STATS ANNUELLES                           #
#                                                                       #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #


# Commencer une requete SQL 'query' pour récupérer le nombre de clients
def sql_nbClt():
    query = [
        'SELECT Count(*) FROM Client WHERE id IN (SELECT f.idClient FROM Facture f WHERE TRUE',
        ') AND idMagasinVDSA IN (SELECT f.idMagasinVDSA FROM Facture f WHERE TRUE',
        ')'
    ]
    return query



""" obtenir le nombre de client inscrit durant une année """
# 'year': entier, année désiré. 2017 pour 2017-2018
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> entier, nombre de clients dont la date d'inscription est antérieur à une année (mois et jour de date_max)
def sql_nbCltOfYear(year, date_max, filter):
    query = sql_nbClt()
    (query[0], params)=sql_addFilter(filter, query[0], [])
    (query[1], params)=sql_addFilter(filter, query[1], params)
    query[2] += ' AND date_inscription <= %s'
    query = ''.join(query)
    params += [dtDate(year+1, date_max.month, date_max.day)]
    return sql_execQuery(query, params, False)[0]



""" obtenir le nombre de nouveaux clients d'une année """
# 'year': entier, année désiré. 2017 pour 2017-2018
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> entier, nombre de clients dont la date d'inscription est entre la date de début et de fin d'une année (mois et jour de date_max)
def sql_nbNewCltOfYear(year, date_max, filter):
    (month, day) = (date_max.month, date_max.day)
    query = sql_nbClt()
    (query[0], params)=sql_addFilter(filter, query[0], [])
    (query[1], params)=sql_addFilter(filter, query[1], params)
    query += ' AND date_inscription >= %s AND date_inscription <= %s'
    query = ''.join(query)
    params += [dtDate(year, month, day), dtDate(year+1, month, day)]
    return sql_execQuery(query, params, False)[0]



""" obtenir la somme du chiffre d'affaire sur une année """
# 'year': entier, année désiré. 2017 pour 2017-2018
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> décimal, somme du CA
def sql_caOfYear(year, date_max, filter):
    (month, day) = (date_max.month, date_max.day)
    query='SELECT SUM(f.montant) FROM Facture f WHERE f.date >= %s AND f.date <= %s'
    params = [dtDate(year, month, day), dtDate(year+1, month, day)]
    (query, params) = sql_addFilter(filter, query, params)
    sum_ca = sql_execQuery(query, params, False)[0]
    return decimalToFloat(sum_ca)



""" obtenir la marge d'une année """
# 'year': entiers, année et mois désirés
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> décimal, infinie ou None, marge de l'année. None si aucune donnée
def sql_margeOfYear(year, date_max, filter):
    (month, day) = (date_max.month, date_max.day)
    query = "SELECT f.montant, f.marge FROM Facture f WHERE f.date >= %s AND f.date <= %s"
    params = [dtDate(year, month, day), dtDate(year+1, month, day)]
    (query, params) = sql_addFilter(filter, query, params)
    marge = calcMarge(sql_execQuery(query, params, True))
    return decimalToFloat(marge)






# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
#                                                                       #
#                    REQUETES STATS MENSUELLES                          #
#                                                                       #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #


""" obtenir le nombre de clients inscrit pour un mois donné """
# 'year', 'month': entiers, année et mois désirés
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> entier ou None, nombre de clients, None si hors du graph
def sql_nbCltOfMonth(year, month, date_max, filter):
    date_end_month = sql_getRangeOfMonth(year, month, date_max)[1]
    if (not date_end_month):
        return None
    query = 'SELECT COUNT(clt.idMagasinVDSA, clt.id) FROM Client clt WHERE clt.date_inscription <= %s'
    params = [dtDate(year, month, date_end_month.day)]
    (query, params)=sql_addFilter(filter, query, params)
    return sql_execQuery(query, params, False)[0]








# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
#                                                                       #
#                         REQUETES GEOLOC                               #
#                                                                       #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #



# Ajoute une jointure à la table Localisation en passant par les clients pour une requete sur les factures
def sql_addGeoloc(query):
    query+=(' FROM Facture f, Localisation l, Client clt '+
        'WHERE f.idClient = clt.id AND f.idMagasinVDSA = clt.idMagasinVDSA AND clt.idLocalisation = l.id')
    return query


# Convertie en listes les données de géoloc sous forme de n-uplets renvoyés par 'sql_execQuery'
def geoDataSqlToList(sql_data):
    len_sql_data = len(sql_data)
    list = [[None] * 4 ] * len_sql_data
    for i in range(len_sql_data):
        list[i] = {
            "id_loc":sql_data[i][0], "cp":sql_data[i][1],
            "ville": sql_data[i][2], "value":decimalToFloat(sql_data[i][3])
        }
    return list



""" obtenir les chiffres d'affaires géolocalisé """
# 'year': entier, année désiré. 2017 pour 2017-2018
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> n-uplet de quadruplets contenant:
#           [0] entier, l'id de la localisation; [1] entier, le code postale; [2] chaine, le nom de la ville; [3] entier, la valeur du CA
def sql_geolocCA(year, date_max, filter):
    query = "SELECT l.id, l.cp, l.ville, SUM(f.montant)"
    query = sql_addGeoloc(query)

    (month, day) = (date_max.month, date_max.day)
    query += ' AND f.date >= %s AND f.date <= %s'
    params = [dtDate(year, month, day), dtDate(year+1, month, day)]

    (query, params) = sql_addFilter(filter, query, params)

    query += ' GROUP BY l.id'
    data = sql_execQuery(query, params, True)
    return geoDataSqlToList(data)



""" obtenir les marges géolocalisé """
# 'year': entier, année désiré. 2017 pour 2017-2018
# 'date_max': objet date, s'obtient avec la fonction getDateMax
# 'filter': liste de 4 entiers 1 char. Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
# ---> n-uplet de quadruplets contenant:
#           [0] entier, l'id de la localisation; [1] entier, le code postale; [2] chaine, le nom de la ville; [3] entier, la valeur de la marge
def sql_geolocMarge(year, date_max, filter):
    t_marge_geoloc = []
    t_loc = sql_execQuery('SELECT l.id, l.cp, l.ville FROM Localisation l', [], True)

    query = "SELECT f.montant, f.marge"
    query = sql_addGeoloc(query)

    (month, day) = (date_max.month, date_max.day)
    query += ' AND f.date >= %s AND f.date <= %s'
    params = [dtDate(year, month, day), dtDate(year+1, month, day)]

    (query, params) = sql_addFilter(filter, query, params)

    query += ' AND l.id = %s'

    for elt in t_loc:
        id_loc = elt[0]
        cp = elt[1]
        ville = elt[2]
        marge = calcMarge(sql_execQuery(query, params + [id_loc], True))
        if marge != None:
            t_marge_geoloc.append( (id_loc, cp, ville, marge) )

    return geoDataSqlToList(t_marge_geoloc)
