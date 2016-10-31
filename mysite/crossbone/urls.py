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

    url(r'^curso/get/(.+)/$', views.events.course, name='evento'),
    url(r'^curso/novo$', views.events.new_course, name='curso_novo'),

    url(r'^disciplina/get/(.+)/$', views.events.subject, name='disciplina'),
    url(r'^disciplina/novo$', views.events.new_subject, name='curso_novo'),

    #Grupos
    url(r'^grupo/get/(.+)/$', views.groups.group, name='grupo'),
    url(r'^grupo/novo$', views.groups.group_new, name='grupo_novo'),
    url(r'^tipogrupo/novo$', views.groups.grouptype_new, name='tipogrupo_novo'),


    #ajax
    url(r'usuarios_roles_list$', views.users.usuarios_roles_list, name='usuarios_roles_list'),

    #ajax
    url(r'usuarios_tasks_list/(.+)/$', views.users.usuarios_tasks_list, name='usuarios_tasks_list'),



    url(r'^stepper$', views.events.stepper, name='stepper'),


]