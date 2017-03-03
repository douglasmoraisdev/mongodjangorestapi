from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home.index, name='home'),
    url(r'^login$', views.home.loginLogout, name='login'),
    url(r'^logout$', views.home.loginLogout, name='logout'),

    #ajax
    url(r'^globalsearch/(.+)/$', views.home.global_search, name='overview_globalsearch'),


]