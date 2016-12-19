from django.conf.urls import url

from . import views

urlpatterns = [
	
    #Celulas
    url(r'^get/(.+)/$', views.cells.cell, name='cell'),    
    url(r'^novo$', views.cells.cell_new, name='cell_new'),
    url(r'^editar/(.+)/$', views.cells.cell_edit, name='cell_edit'),


]