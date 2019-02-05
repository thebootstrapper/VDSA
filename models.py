# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib import admin


class Admin(models.Model):
    email = models.CharField(max_length=64)
    mdp = models.CharField(max_length=64)
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
    mdp = models.CharField(max_length=64)
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
    mdp_directeur = models.CharField(max_length=64, blank=True, null=True)
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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
    #=read only     managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
#=read only         managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
#=read only         managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
#=read only         managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
    #=read only     managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
#=read only         managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
#=read only         managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
#=read only         managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
#=read only         managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
#=read only         managed = False
        db_table = 'django_session'
