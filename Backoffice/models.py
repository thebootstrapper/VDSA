from __future__ import absolute_import
from django.db import models
from django.contrib import admin
from con_ins.choices import *


class File(models.Model):
    source= models.FileField()

class Admin(models.Model):
    email = models.CharField(max_length=64)
    mdp = models.CharField(max_length=64, editable=False)
    nom = models.CharField(max_length=64, blank=True, null=True)
    prenom = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
#=read only        managed = False
        db_table = 'Admin'


class Client(models.Model):
    idmagasinvdsa = models.ForeignKey('Magasinvdsa', models.DO_NOTHING, db_column='idMagasinVDSA')  # Field name made lowercase.
    id = models.PositiveIntegerField(primary_key=True)
    date_inscription = models.DateField(blank=True, null=True)
    idlocalisation = models.ForeignKey('Localisation', models.DO_NOTHING, db_column='idLocalisation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
#=read only         managed = False
        db_table = 'Client'
        unique_together = (('id', 'idmagasinvdsa'),)


class Commercial(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    email = models.CharField(max_length=64)
    mdp = models.CharField(max_length=64, editable=False)
    nom = models.CharField(max_length=64, blank=True, null=True)
    prenom = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
#=read only         managed = False
        db_table = 'Commercial'


class Facture(models.Model):
    date = models.DateField(blank=True, null=True)
    montant = models.DecimalField(max_digits=14, decimal_places=2)
    marge = models.DecimalField(max_digits=11, decimal_places=2)
    idclient = models.ForeignKey(Client, models.DO_NOTHING, db_column='idClient')  # Field name made lowercase.
    idmagasinvdsa = models.CharField(db_column='idMagasinVDSA', max_length=1)  # Field name made lowercase.
    idsousfamille = models.ForeignKey('Sousfamille', models.DO_NOTHING, db_column='idSousFamille', blank=True, null=True)  # Field name made lowercase.
    idcommercial = models.ForeignKey(Commercial, models.DO_NOTHING, db_column='idCommercial')  # Field name made lowercase.

    class Meta:
#=read only         managed = False
        db_table = 'Facture'


class Famille(models.Model):
    nom = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
#=read only         managed = False
        db_table = 'Famille'


class Localisation(models.Model):
    cp = models.PositiveIntegerField()
    ville = models.CharField(max_length=64)

    class Meta:
#=read only         managed = False
        db_table = 'Localisation'


class Magasinvdsa(models.Model):
    id = models.CharField(primary_key=True, max_length=1)
    nom_magasin = models.CharField(max_length=64)
    email_directeur = models.CharField(max_length=64, blank=True, null=True)
    mdp_directeur = models.CharField(max_length=64, blank=True, null=True, editable=False)
    nom_directeur = models.CharField(max_length=64, blank=True, null=True)
    prenom_directeur = models.CharField(max_length=64, blank=True, null=True)
    idlocalisation = models.ForeignKey(Localisation, models.DO_NOTHING, db_column='idLocalisation')  # Field name made lowercase.

    class Meta:
#=read only         managed = False
        db_table = 'MagasinVDSA'

class Sousfamille(models.Model):
    nom = models.CharField(max_length=64, blank=True, null=True)
    idfamille = models.ForeignKey(Famille, models.DO_NOTHING, db_column='idFamille', blank=True, null=True)  # Field name made lowercase.

    class Meta:
#=read only         managed = False
        db_table = 'SousFamille'

# classe de session des utilisateurs

class Session_utilisateur(models.Model):
  email_s = models.CharField(max_length=100)
  statut_s = models.CharField(max_length=100)

# classe des choix d'inscription

class Statut(models.Model):
  statuts = models.IntegerField(choices=CHOIX_STATUT, default=1)
