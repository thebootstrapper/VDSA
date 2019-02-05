"""VDSA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings

from . import views


#pour l'importation de fichier
from django.conf.urls.static import static


urlpatterns = [
    #/geoloc/
    url(r'^geoloc/',include('Geolocalisation.urls')),
    #/dashboard/
    url(r'^dashboard/',include('Dashboard.urls')),
    #/Dashboard/
    url(r'^con_ins/',include('con_ins.urls')),

    url(r'^backoffice/',include('Backoffice.urls')),

    url(r'^admin',admin.site.urls),

    #racine
    url(r'^',include('con_ins.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

    #pour l'importation de fichier
    urlpatterns += static(settings.STATIC_URL, document_rool=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_rool=settings.MEDIA_ROOT)
