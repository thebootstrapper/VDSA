from django.shortcuts import render
from django.http import HttpResponse


from . import lecture_fichier as lect

def lecture_fichier(request):
	lect.main()
	return render(request, 'dashboard/dashboard.html')
