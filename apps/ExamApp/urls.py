from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.add, name='add_trip'),
    url(r'^create$', views.create, name='create_trip'),
    url(r'^destination/(?P<trip_id>\d+)$', views.view, name="view_trip"),
    url(r'^destination/(?P<trip_id>\d+)/join$', views.join, name='join_trip')
]