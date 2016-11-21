from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home.index, name='index'),
    url(r'^login$', views.home.loginLogout, name='login'),
    url(r'^logout$', views.home.loginLogout, name='logout'),


    url(r'^usuario/get/(.+)/$', views.users.user, name='user'),
    url(r'^usuario/novo$', views.users.user_new, name='user_novo'),

    url(r'^funcao/novo$', views.roles.role_new, name='funcao_novo'),

    url(r'^atividade/get/(.+)/$', views.tasks.task, name='atividade'),
    url(r'^atividade/novo$', views.tasks.task_new, name='atividade_novo'),



    #Eventos e Cursos
    url(r'^evento/get/(.+)/$', views.events.event, name='evento'),
    url(r'^evento/novo$', views.events.event_new, name='evento_novo'),


    url(r'^reuniaocelula/get/(.+)/$', views.cell_metting.cell_metting, name='cell_metting'),
    url(r'^reuniaocelula/novo$', views.cell_metting.cell_metting_new, name='cell_metting_new'),


    url(r'^curso/get/(.+)/$', views.courses.course, name='curso'),
    url(r'^curso/novo$', views.courses.course_new, name='curso_novo'),


    url(r'^disciplina/get/(.+)/$', views.courses.subject, name='subject'),
    url(r'^disciplina/novo/(.+)/$', views.courses.subject_new, name='subject_new'),



    #Grupos
    url(r'^grupo/get/(.+)/$', views.groups.group, name='grupo'),
    url(r'^grupo/novo$', views.groups.group_new, name='grupo_novo'),
    url(r'^tipogrupo/novo$', views.groups.grouptype_new, name='tipogrupo_novo'),



    #Celulas
    url(r'^celula/get/(.+)/$', views.cells.cell, name='celula'),    
    url(r'^celula/novo$', views.cells.cell_new, name='celula_novo'),
    url(r'^celula/editar/(.+)/$', views.cells.cell_edit, name='celula_editar'),



    #ajax
    url(r'usuarios_roles_list$', views.users.usuarios_roles_list, name='usuarios_roles_list'),

    #ajax
    url(r'usuarios_tasks_list/(.+)/$', views.users.usuarios_tasks_list, name='usuarios_tasks_list'),

    #ajax
    url(r'^get_servant_autocomplete$', views.users.get_servant_autocomplete, name='servos_autocomplete'),

    #ajax
    url(r'^add_servant_list$', views.users.add_servant_list, name='servos_add_list'),


    #ajax
    url(r'^get_member_autocomplete$', views.users.get_member_autocomplete, name='membro_autocomplete'),

    #ajax
    url(r'^add_member_list$', views.users.add_member_list, name='membro_add_list'),

    #ajax
    url(r'day_group_hmtl_frag$', views.users.day_group_hmtl_frag, name='day_group_hmtl_frag'),    




]