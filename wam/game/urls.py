from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^successful_upload/$', views.successful_upload, name='successful_upload')
)
