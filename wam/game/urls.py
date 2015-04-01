from django.conf.urls import patterns, url
from django.conf.urls.static import static

from game import views
from game import play
from game import user

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^registration/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^challenge_user/$', play.challenge_user, name ='challenge_user'),
    url(r'^play/$', play.play, name='play'),
    url(r'^view_user_ai/$', play.view_user_ai, name='view_user_ai'),
    url(r'^view_user_profile/$', user.view_user_profile, name='view_user_profile'),  
    url(r'^forgot_password/$', user.forgot_password, name='forgot_password'),   
    url(r'^view_code/$', user.view_code, name='view_code')                
)
