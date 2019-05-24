from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create_user),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^trips/new$', views.new_trip),
    url(r'^logout$', views.logout),
    url(r'^create_trip$', views.create_trip),
    url(r'^edit_trip$', views.edit_trip),
    url(r'^remove/(?P<my_val>\d+)$', views.remove),
    url(r'^trips/edit/(?P<my_val>\d+)$', views.edit),
    url(r'^trips/(?P<my_val>\d+)$', views.show_trip),
    url(r'^trips/join/(?P<my_val>\d+)$', views.join),
    url(r'^cancel/(?P<my_val>\d+)$', views.cancel),
]