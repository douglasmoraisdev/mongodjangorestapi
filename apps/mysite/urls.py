"""apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from cell.views import *

urlpatterns = [
    url(r'^', include('bethel_core.urls')),
    url(r'^bethel_core/', include('bethel_core.urls')),
    url(r'^celula/', include('cell.urls')),
    url(r'^reuniaocelula/', include('cell_metting.urls')),    
    url(r'^usuario/', include('user.urls')),
    url(r'^overview/', include('overview.urls')),
    url(r'^mig/', include('mig.urls')),

    url(r'^admin/', admin.site.urls),
]


#router = routers.DefaultRouter()
#router.register(r'cells', cells_api.CellsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
#    url(r'^', include(cells.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
