from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home.index, name='home'),
    url(r'^login$', views.home.loginLogout, name='login'),
    url(r'^logout$', views.home.loginLogout, name='logout'),

    url(r'^funcao/novo$', views.roles.role_new, name='role_new'),

    url(r'^atividade/get/(.+)/$', views.tasks.task, name='task'),
    url(r'^atividade/novo$', views.tasks.task_new, name='task_new'),


    #Eventos e Cursos
    url(r'^evento/get/(.+)/$', views.events.event, name='event'),
    url(r'^evento/novo$', views.events.event_new, name='event_new'),


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


]