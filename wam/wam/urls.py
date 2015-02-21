from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.site.site_header = 'WAM administration'

urlpatterns = patterns('',
    url(r'^game/', include('game.urls', namespace='game')),
    url(r'^admin/', include(admin.site.urls)),
)
