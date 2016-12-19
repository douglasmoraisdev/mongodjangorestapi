from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^get/(.+)/$', views.base_event_app.base_event_app, name='base_event_app'),
    url(r'^novo/(.+)/$', views.base_event_app.base_event_app_new, name='base_event_app_new'),
    url(r'^editar/(.+)/(.+)/$', views.base_event_app.base_event_app_edit, name='base_event_app_edit'),


]