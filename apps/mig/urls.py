from django.conf.urls import url

from . import views

urlpatterns = [
	
    #Celulas
    url(r'^prover/$', views.mig.prover, name='mig_prover'),


]