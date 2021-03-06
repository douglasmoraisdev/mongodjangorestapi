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
from rest_framework_mongoengine import routers

from cell.views import *
from cell_metting.views import *
from user.views import *
from core.views import *



router = routers.DefaultRouter()

router.register(r'core', core_api.BethelCoreViewSet)

router.register(r'celula', cells_api.CellsViewSet)
router.register(r'reuniaocelula', cell_metting_api.CellMettingsViewSet)
router.register(r'usuario', users_api.UsersViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^admin/', admin.site.urls),
    
    url(r'^mig/', include('mig.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    url(r'^accounts/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),    
]

