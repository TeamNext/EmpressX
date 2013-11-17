from django.conf.urls import patterns, include, url

urlpatterns = patterns('bpm.contrib.auth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)
