# -*- coding: utf-8 -*-

from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# 随从执行命令后的回调接口, 统一使用xmlrpc方式
urlpatterns = patterns('empressx.empress.views',
    url(r'^xmlrpc/', 'xmlrpc_handler'),
)

