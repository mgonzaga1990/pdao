"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from person.views import *

admin.site.site_header = 'PDAO - KRDBMIS'  # default: "Django Administration"
admin.site.index_title = 'Features menu'  # default: "Site administration"
admin.site.site_title = 'Admin Panel | PDAO'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
    
                  url(r'^evaluation/', include("evaluation.urls")),
                  url(r'^events/', include("events.urls")),

                #   ajax section
                  path('ajax/fetch_brgy/<municipal_id>', fetch_brgy , name='validate_username'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
