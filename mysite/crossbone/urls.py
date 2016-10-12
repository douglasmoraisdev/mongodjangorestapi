from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'novogrupo$', views.novogrupo, name='novogrupo'),
    url(r'novouser$', views.novouser, name='novouser'),  
    url(r'novorole$', views.novorole, name='novorole'),
    url(r'novogrouptype$', views.novogrouptype, name='novogrouptype'),


    url(r'usuarios_roles_list$', views.usuarios_roles_list, name='usuarios_roles_list'),

    
]
