# coding=utf-8

from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


urlpatterns = patterns('empress.views',
    url(r'^get_websvr_list/$', 'get_websvr_list'),
    url(r'^get_server_app_list/$', 'get_server_app_list'),
)

