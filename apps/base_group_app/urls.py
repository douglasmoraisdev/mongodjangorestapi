from django.conf.urls import url

from . import views

urlpatterns = [
	
    #Celulas
    url(r'^get/(.+)/$', views.base_group_app.base_group_app, name='base_group_app'),    
    url(r'^novo$', views.base_group_app.base_group_app_new, name='base_group_app_new'),
    url(r'^editar/(.+)/$', views.base_group_app.base_group_app_edit, name='base_group_app_edit'),


]