from django.conf.urls import url

from . import views

urlpatterns = [
 

    url(r'^get/(.+)/$', views.users.user, name='user'),
    url(r'^novo$', views.users.user_new, name='user_new'),

    #ajax
    url(r'usuarios_roles_list$', views.users.usuarios_roles_list, name='usuarios_roles_list'),

    #ajax
    url(r'usuarios_tasks_list/(.+)/$', views.users.usuarios_tasks_list, name='usuarios_tasks_list'),

    #ajax
    url(r'^get_servant_autocomplete$', views.users.get_servant_autocomplete, name='get_servant_autocomplete'),

    #ajax
    url(r'^add_servant_list$', views.users.add_servant_list, name='add_servant_list'),

    #ajax
    url(r'^add_servant_list_presence$', views.users.add_servant_list_presence, name='add_servant_list_presence'),    

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