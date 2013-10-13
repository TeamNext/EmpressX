from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^xmlrpc/', 'empressx.retinue.views.xmlrpc_handler'),
)
