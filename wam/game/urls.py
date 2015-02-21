from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^successful_upload/$', views.successful_upload, name='successful_upload'),
    url(r'^play/$', views.play, name='play'),
    url(r'^registration/$', views.register, name='register'),
    url(r'^successful_registeration/$', views.successful_registeration, name='successful_registeration'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout')
)
