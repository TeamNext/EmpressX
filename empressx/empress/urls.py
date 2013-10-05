# -*- coding: utf-8 -*-

from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


urlpatterns = patterns('empress.views',
	url(r'^callback/$', 'mission_report'),    # 随从执行命令后的回调接口, todo: 换成xmlrpc方式
)

