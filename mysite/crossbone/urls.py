from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login$', views.loginLogout, name='login'),

    url(r'usuario/novo$', views.user_new, name='user_novo'),

    url(r'funcao/novo$', views.role_new, name='funcao_novo'),

    url(r'tipogrupo/novo$', views.grouptype_new, name='tipogrupo_novo'),

    url(r'evento$', views.event, name='evento'),    
    url(r'evento/novo$', views.event_new, name='evento_novo'),

    url(r'grupo$', views.group, name='grupo'),
    url(r'^grupo/novo$', views.group_new, name='grupo_novo'),


    #ajax
    url(r'usuarios_roles_list$', views.usuarios_roles_list, name='usuarios_roles_list'),

    
]