from django.conf.urls import patterns, url

from game import views
from game import play

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^registration/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^challenge_user/$', play.challenge_users_ai, name ='challenge_user'),
    url(r'^play/$', play.play, name='play'),
)
