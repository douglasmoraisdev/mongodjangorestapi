from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home.index, name='index'),
    url(r'login$', views.home.loginLogout, name='login'),

    url(r'usuario/novo$', views.users.user_new, name='user_novo'),

    url(r'funcao/novo$', views.roles.role_new, name='funcao_novo'),

    url(r'evento$', views.events.event, name='evento'),    
    url(r'evento/novo$', views.events.event_new, name='evento_novo'),

    url(r'grupo$', views.groups.group, name='grupo'),
    url(r'^grupo/novo$', views.groups.group_new, name='grupo_novo'),
    url(r'tipogrupo/novo$', views.groups.grouptype_new, name='tipogrupo_novo'),


    #ajax
    url(r'usuarios_roles_list$', views.users.usuarios_roles_list, name='usuarios_roles_list'),

    
]