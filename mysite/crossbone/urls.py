from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login$', views.loginLogout, name='login'),
    

    url(r'grupo$', views.group, name='grupo'),
    url(r'^grupo/novo$', views.group_new, name='grupo_novo'),

    url(r'usuario/novo$', views.user_new, name='user_novo'),

    url(r'funcao/novo$', views.role_new, name='funcao_novo'),

    url(r'tipogrupo/novo$', views.grouptype_new, name='tipogrupo_novo'),


    url(r'evento$', views.event, name='evento'),    


    url(r'novogrupo$', views.novogrupo, name='novogrupo'),
    url(r'novouser$', views.novouser, name='novouser'),  
    url(r'novorole$', views.novorole, name='novorole'),
    url(r'novogrouptype$', views.novogrouptype, name='novogrouptype'),
    url(r'newevent$', views.newevent, name='newevent'),    


    url(r'usuarios_roles_list$', views.usuarios_roles_list, name='usuarios_roles_list'),

    
]
