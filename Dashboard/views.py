from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request,"Dashboard/dashboard.html")

# Create your views here.
