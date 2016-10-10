from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contato/$', views.contact, name='contact'),
    url(r'^novo/$', views.novo, name='novo'),
    url(r'^empregados/$', views.empregados, name='empregados'),    
]
