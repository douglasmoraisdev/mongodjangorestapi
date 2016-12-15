from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home.index, name='home'),
 

    #Celulas
    url(r'^(.+)/$', views.cells.cell, name='cell'),    
    url(r'^celula/get/(.+)/$', views.cells.cell, name='cell'),    
    url(r'^celula/novo$', views.cells.cell_new, name='cell_new'),
    url(r'^celula/editar/(.+)/$', views.cells.cell_edit, name='cell_edit'),


]