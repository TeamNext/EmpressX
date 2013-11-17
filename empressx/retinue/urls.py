from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'empressx.retinue.views.xmlrpc_handler'),
)
