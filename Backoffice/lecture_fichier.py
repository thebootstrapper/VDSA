
import os
import time
from datetime import date
from .models import*


def enlevet (l):
    for i in range(len(l)):
        (l[i]).rstrip('\t')
    return l

def print_liste (l):
    for i in range(len(l)):
        print(l[i])
        print('       ')
def print_liste_liste (l):
    for i in range(len(l)):
        print_liste(l[i])
        print('\n\n\n')

def separe_ligne (l):
    for i in range(len(l)):
        l2=l[i].split(";")
        l[i]=l2
    return l

def est_int(mot):
    if (mot[0]=="0") or (mot[0]=="1") or(mot[0]=="2") or(mot[0]=="3") or(mot[0]=="4") or(mot[0]=="5") or(mot[0]=="6") or (mot[0]=="7") or (mot[0]=="8") or (mot[0]=="9"):
        return True
    else :
        return False

def verif_dec(mot):
    if not(',' in mot):
        return float(mot)
    elif not('.' in mot):
        mot=mot.split(",")
        tmp=mot[1]
        mot[1]='.'
        mot.append(tmp)
        mot=''.join(mot)
        return float(mot)
    else:
        mot=mot.split(",")
        mot=''.join(mot)
        return float(mot)

def est_vide(mot):
    if (mot=='') or (mot=='.'):
        return True
    else:
        return False



def entrer_commercial(l):
    for i in range(1,(len(l)-1)):
        if (Commercial.objects.filter(id=int(l[i][0])).count())==0:
            print("entrer du commercial n°",i," dans la base de donnée")
            try :
                Commercial(
                id=int(l[i][0]),
                email="",
                mdp="",
                nom= "",
                prenom= "",
                ).save()
            except :
                print("ca ne marche pas")

def entrer_famille(l):
    for i in range(1,(len(l)-1)):
        if ((Famille.objects.filter(nom=l[i][2]).count())==0) and (est_int(l[i][2])==False):
            try:
                print("entrer de la famille n°",i," dans la base de donnée")
                Famille(
                nom=l[i][2]
                ).save()
            except:
                print("ca ne marche pas famille")

def entrer_localisation(l):
    for i in range(1,(len(l)-1)):
        if ((Localisation.objects.filter(ville=(l[i][5])).count())==0) and (est_vide(l[i][5])==False):
            try:
                print("entrer de la localisation n°",i," dans la base de donnée")
                Localisation(
                cp=int(l[i][4]),
                ville=l[i][5]
                ).save()
            except:
                print("ca ne marche pas localisation")

def entrer_sousFam(l):
    for i in range(1,(len(l)-1)):
        if ((Sousfamille.objects.filter(nom=l[i][3]).count())==0) and (est_int(l[i][2])==False):
            tmp=(Famille.objects.get(nom=l[i][2]))
            print("entrer de la SousFamille n°",i," dans la base de donnée")
            try:
                Sousfamille(
                nom=l[i][3],
                idfamille=tmp
                ).save()
            except:
                print("ca ne marche pas sous famille")

def entrer_client(l):
    for i in range(1,(len(l)-1)):
        codeClient=l[i][1]

        if ((Client.objects.filter(id=(int(codeClient[1:])),idmagasinvdsa=codeClient[0]).count())==0) and (est_vide(l[i][5])==False):
            tmp_mag=(Magasinvdsa.objects.get(id=codeClient[0]))
            tmp_loc=(Localisation.objects.get(ville=l[i][5]))
            tmp_date=l[i][6].split("/")
            print("entrer du client n°",i," dans la base de donnée")
            try:
                Client(
                idmagasinvdsa=tmp_mag,
                id=int(codeClient[1:]),
                date_inscription=date(int(tmp_date[2]),int(tmp_date[1]),int(tmp_date[0])),
                idlocalisation=tmp_loc
                ).save()
            except:
                print("ca ne marche pas Client")
        elif ((Client.objects.filter(id=(int(codeClient[1:])),idmagasinvdsa=codeClient[0]).count())==0) and (est_vide(l[i][5])==True):
            print("entrer du client n°",i," dans la base de donnée")
            if codeClient[0]=="V":
                tmp_loc=(Localisation.objects.get(ville="Cergy"))

            else:
                tmp_loc=(Localisation.objects.get(ville="Paris"))

            tmp_mag=(Magasinvdsa.objects.get(id=codeClient[0]))
            tmp_date=l[i][6].split("/")
            try:
                Client(
                idmagasinvdsa=tmp_mag,
                id=int(codeClient[1:]),
                date_inscription=date(int(tmp_date[2]),int(tmp_date[1]),int(tmp_date[0])),
                idlocalisation=tmp_loc
                ).save()
            except:
                print("ca ne marche pas Client")
        else:

            tmp_date=l[i][6].split("/")
            exist=(Client.objects.filter(id=(int(codeClient[1:])),idmagasinvdsa=codeClient[0]))[0]
            date_exist=exist.date_inscription
            if date_exist > (date(int(tmp_date[2]),int(tmp_date[1]),int(tmp_date[0]))) :
                print("actualisation du Client n°",i," dans la base de donnée")
                exist.date_inscription=date(int(tmp_date[2]),int(tmp_date[1]),int(tmp_date[0]))
                exist.save()

def entrer_Facture (l):
    for i in range(1,(len(l)-1)):
        codeClient=l[i][1]
        tmp_date=l[i][6].split("/")
        if ((Facture.objects.filter(date=date(int(tmp_date[2]),int(tmp_date[1]),int(tmp_date[0])),montant=verif_dec(l[i][7]),marge=verif_dec(l[i][8]),idclient=codeClient[1:],idmagasinvdsa=codeClient[0]).count())==0) and (est_int(l[i][2])==False):
            tmp_client=(Client.objects.get(id=codeClient[1:]))
            tmp_sous=(Sousfamille.objects.get(nom=l[i][3]))
            tmp_com=(Commercial.objects.get(id=l[i][0]))
            print("entrer de la Facture n°",i," dans la base de donnée")
            try:
                Facture(
                date= date(int(tmp_date[2]),int(tmp_date[1]),int(tmp_date[0])),
                montant= verif_dec(l[i][7]),
                marge= verif_dec(l[i][8]),
                idclient=tmp_client,
                idmagasinvdsa= codeClient[0],
                idsousfamille=tmp_sous,
                idcommercial=tmp_com
                ).save()
            except:
                print("ca ne marche pas Facture")








"""
def liste_str_to_int (l,id_colonne):
    for i in range(len()):
        l[i][id_colonne]=int(l[i][id_colonne])

def ligne_element_vide (l,i,bool):
    if i==(len(l)):
        return bool
    else:
        if (l[i].isspace())==True:
            print(i)
            bool=True
            return bool
        else:
            print(i)
            return ligne_element_vide(l,i+1,bool)


def verif_element_vide(l):
    for i in range(len(l)):
        if bool==True:
            del l[i]
    return l
"""

def ouvrir_fichier():

    try:

        obFichier = open("./media/exemple.csv",'r',encoding='cp1252')
        liste = []
        lister = []
        essai = ["aaaa","bbbbb","    ","            ","cccc"]
        while 1:
          t=obFichier.readline()
          if not t:
              break
          else :
           liste.append(t.rstrip("\n").rstrip('\t'))
        lister=separe_ligne(liste)

    except IOError:
        print ("Ce fichier n'existe pas")
    entrer_commercial(liste)
    entrer_famille(liste)
    entrer_localisation(liste)
    entrer_sousFam(liste)
    entrer_client(liste)
    entrer_Facture(liste)
    print("Votre fichier a bien été charger dans la base de donnée")






"""print_liste(lister)"""
def main():

    ouvrir_fichier()
    print('cbon')
