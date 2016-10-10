from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contato/$', views.contact, name='contact'),
    url(r'^novogrupo/$', views.novogrupo, name='novogrupo'),
    url(r'^novouser/$', views.novouser, name='novouser'),    
    url(r'^novorole/$', views.novorole, name='novorole'),    
    url(r'^userrole/$', views.userrole, name='userrole'),
    url(r'^visualizar/$', views.visualizar, name='visualizar'),    
]
