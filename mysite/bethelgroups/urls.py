from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home.index, name='home'),
    url(r'^login$', views.home.loginLogout, name='login'),
    url(r'^logout$', views.home.loginLogout, name='logout'),


    url(r'^usuario/get/(.+)/$', views.users.user, name='user'),
    url(r'^usuario/novo$', views.users.user_new, name='user_new'),

    url(r'^funcao/novo$', views.roles.role_new, name='role_new'),

    url(r'^atividade/get/(.+)/$', views.tasks.task, name='task'),
    url(r'^atividade/novo$', views.tasks.task_new, name='task_new'),



    #Eventos e Cursos
    url(r'^evento/get/(.+)/$', views.events.event, name='event'),
    url(r'^evento/novo$', views.events.event_new, name='event_new'),


    url(r'^reuniaocelula/get/(.+)/$', views.cell_metting.cell_metting, name='cell_metting'),
    url(r'^reuniaocelula/novo/(.+)/$', views.cell_metting.cell_metting_new, name='cell_metting_new'),
    url(r'^reuniaocelula/editar/(.+)/(.+)/$', views.cell_metting.cell_metting_edit, name='cell_metting_edit'),


    url(r'^curso/get/(.+)/$', views.courses.course, name='course'),
    url(r'^curso/novo$', views.courses.course_new, name='course_new'),
    url(r'^curso/editar/(.+)/$', views.courses.course_edit, name='course_edit'),


    url(r'^disciplina/get/(.+)/$', views.subjects.subject, name='subject'),
    url(r'^disciplina/novo/(.+)/$', views.subjects.subject_new, name='subject_new'),
    url(r'^disciplina/editar/(.+)/(.+)/$', views.subjects.subject_edit, name='subject_edit'),



    #Grupos
    url(r'^grupo/get/(.+)/$', views.groups.group, name='group'),
    url(r'^grupo/novo$', views.groups.group_new, name='group_new'),
    url(r'^tipogrupo/novo$', views.groups.grouptype_new, name='grouptype_new'),



    #Celulas
    url(r'^celula/get/(.+)/$', views.cells.cell, name='cell'),    
    url(r'^celula/novo$', views.cells.cell_new, name='cell_new'),
    url(r'^celula/editar/(.+)/$', views.cells.cell_edit, name='cell_edit'),



    #ajax
    url(r'usuarios_roles_list$', views.users.usuarios_roles_list, name='usuarios_roles_list'),

    #ajax
    url(r'usuarios_tasks_list/(.+)/$', views.users.usuarios_tasks_list, name='usuarios_tasks_list'),

    #ajax
    url(r'^get_servant_autocomplete$', views.users.get_servant_autocomplete, name='get_servant_autocomplete'),

    #ajax
    url(r'^add_servant_list$', views.users.add_servant_list, name='add_servant_list'),

    #ajax
    url(r'^get_member_autocomplete$', views.users.get_member_autocomplete, name='get_member_autocomplete'),

    #ajax
    url(r'^add_member_list$', views.users.add_member_list, name='add_member_list'),

    #ajax
    url(r'^add_member_list_presence$', views.users.add_member_list_presence, name='add_member_list_presence'),

    #ajax
    url(r'^add_member_list_save$', views.users.add_member_list_save, name='add_member_list_save'),

    #ajax
    url(r'^remove_member_list_save$', views.users.remove_member_list_save, name='remove_member_list_save'),

    #ajax
    url(r'day_group_hmtl_frag$', views.users.day_group_hmtl_frag, name='day_group_hmtl_frag'),    




]