from __future__ import absolute_import
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import Connexion_form
from .forms import Inscription_form
from Backoffice.models import Commercial
from Backoffice.models import Magasinvdsa
from Backoffice.models import Session_utilisateur
from Backoffice.models import Admin


def connexion_view(request):

  form = Connexion_form(request.POST or None)
  Session_utilisateur.objects.all().delete()
  con_ins_state = 0 # 0 si jamais essayé, 1 si connecté comme commercial, 2 si connecté comme directeur, 3 si connecté comme administrateur, -1 si connexion invalide

  if form.is_valid():
    email_form = form.cleaned_data['email']
    password_form = form.cleaned_data['password']


    com_count = Commercial.objects.filter(email=email_form, mdp=password_form).count()
    dir_count = Magasinvdsa.objects.filter(email_directeur=email_form, mdp_directeur=password_form).count()
    adm_count = Admin.objects.filter(email=email_form, mdp=password_form).count()

    if (com_count == 1):
      con_ins_state = 1
      commercial = Session_utilisateur()
      commercial.email_s = email_form
      commercial.statut_s = 'commercial'
      commercial.save()
    elif (dir_count == 1):
      con_ins_state = 2
      directeur = Session_utilisateur()
      directeur.email_s = email_form
      directeur.statut_s = 'directeur'
      directeur.save()
    elif (adm_count == 1):
      con_ins_state = 3
      administrateur = Session_utilisateur()
      administrateur.email_s = email_form
      administrateur.statut_s = 'administrateur'
      administrateur.save()
    else:
      con_ins_state = -1

  return render(request, 'con_ins/connexion.html', locals())






def inscription_view(request):

  form = Inscription_form(request.POST or None)
  con_ins_state = 0 # 0 si jamais essayé, 1 si inscription réussie, -1 si inscription invalide

  if form.is_valid():

    nom_form = form.cleaned_data['nom']
    prenom_form = form.cleaned_data['prenom']
    email_form = form.cleaned_data['email']
    statut_form = int(form.cleaned_data['statut'])
    magasin_form = form.cleaned_data['magasin']

    if (statut_form == 1):
      con_ins_state = 1
      subject = 'Demande d\'inscription VDSA'
      message = 'Nom : '+nom_form+'\n'+'Prénom : '+prenom_form+'\n'+'Email : '+email_form+'\n'+'Statut : commercial'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = ['gestion.vdsa@gmail.com',]

      send_mail(subject,message,email_from,recipient_list)
    else:
      mag_count = Magasinvdsa.objects.filter(nom_magasin=magasin_form).count()
      if (mag_count == 0):
        con_ins_state = -1
      else:
        con_ins_state = 1

        subject = 'Demande d\'inscription VDSA'
        message = 'Nom : '+nom_form+'\n'+'Prénom : '+prenom_form+'\n'+'Email : '+email_form+'\n'+'Statut : magasin'+'\n'+'Magasin : '+magasin_form
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['gestion.vdsa@gmail.com',]

        send_mail(subject,message,email_from,recipient_list)

  return render(request, 'con_ins/inscription.html', locals())
