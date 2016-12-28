from django.conf.urls import url

from . import views

urlpatterns = [
	
    #Home
    url(r'^$', views.overview.home, name='overview_home'),



]