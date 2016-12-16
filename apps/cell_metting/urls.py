from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^get/(.+)/$', views.cell_metting.cell_metting, name='cell_metting'),
    url(r'^novo/(.+)/$', views.cell_metting.cell_metting_new, name='cell_metting_new'),
    url(r'^editar/(.+)/(.+)/$', views.cell_metting.cell_metting_edit, name='cell_metting_edit'),


]