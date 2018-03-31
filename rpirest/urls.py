# -*- coding: utf-8 -*-
"""rpisensehat_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))'/
"""
from django.contrib import admin
from django.conf.urls import url, include

# Snippet para servir ficheros estáticos en modo debug
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^admin/', admin.site.urls),

    #APIs DRF
    url(r'^api/v1/sensehat/', view=include('apirest.urls', namespace='sensehat')),
    url(r'^api/v1/dht11/', include('apirest_dht.urls')),
    url(r'^api/v1/dht22/', include('apirest_dht.urls'), {'device': "dht22"}),
    url(r'^api/v1/am2302/', include('apirest_dht.urls'), {'device': "am2302"}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
