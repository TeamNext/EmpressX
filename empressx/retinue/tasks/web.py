import os
import xmlrpclib

from celery import chain, task
from django.template.loader import render_to_string

from empressx.retinue.conf import settings
from empressx.retinue.utils import localcommand


@task
def reload_nginx(app_name):
    nginx = settings.RETINUE_NGINX_PATH
    conf = settings.RETINUE_NGINX_CONF if settings.RETINUE_NGINX_CONF else 'conf/nginx.conf'
    localcommand("%(nginx)s -s reload -c %(conf)s" % locals())
    return app_name


@task
def delete_config(app_name):
    conf_home = settings.RETINUE_NGINX_UPSTREAM_HOME
    localcommand("rm -f %(conf_home)s/%(app_name)s.conf" % locals())
    return app_name


@task
def generate_config(app_name):
    client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
    app_info = client.app_info(app_name)

    rendered = render_to_string('empressx/retinue/upstream.conf', app_info)

    with open(os.path.join(settings.RETINUE_NGINX_UPSTREAM_HOME, '%s.conf' % app_name), 'w') as f:
        f.write(rendered)

    return app_name


@task(ignore_result=True)
def serve(app_name, uuid):
    chain(generate_config.s(app_name),
          reload_nginx.s()).apply_async()


@task(ignore_result=True)
def unserve(app_name, uuid):
    chain(delete_config.s(app_name)).apply_async()
