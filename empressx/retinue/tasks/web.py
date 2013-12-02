import time
import os
import xmlrpclib

from celery import chain, task
from django.template.loader import render_to_string
from django.core.cache import cache
from django.utils import timezone

from empressx import states
from empressx.retinue.conf import settings
from empressx.retinue.utils import localcommand

from .app import task_tracker


@task
@task_tracker
def reload_nginx(target):
    cache.set('web_nginx_last_reload_request', time.mktime(timezone.now().timetuple()))
    _reload_nginx.apply_async(countdown=5)
    return target


@task(ignore_result=True)
def _reload_nginx():
    last_reload_request = cache.get('web_nginx_last_reload_request')
    now = time.mktime(timezone.now().timetuple())
    if not last_reload_request or now - last_reload_request >= 5:
        nginx_path = settings.ROUTER_NGINX_PATH
        conf = settings.ROUTER_NGINX_CONF if settings.ROUTER_NGINX_CONF else 'conf/nginx.conf'
        localcommand("%(nginx_path)s -s reload -c %(conf)s" % locals())


@task
@task_tracker
def delete_config(target):
    app_info, uuid = target
    app_name = app_info['app_name']

    conf_home = settings.RETINUE_NGINX_UPSTREAM_HOME
    localcommand("rm -f %(conf_home)s/%(app_name)s.conf" % locals())
    return target


@task
@task_tracker
def generate_config(target):
    app_info, uuid = target
    app_name = app_info['app_name']

    rendered = render_to_string('empressx/retinue/upstream.conf', app_info)

    if rendered.strip():
        with open(os.path.join(settings.RETINUE_NGINX_UPSTREAM_HOME, '%s.conf' % app_name), 'w') as f:
            f.write(rendered)

    return target


@task(ignore_result=True)
@task_tracker
def end(target):
    app_info, uuid = target
    rpc_client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)

    rpc_client.private.callback({
        'uuid': uuid,
        'state': states.SUCCESS,
        'data': 'Done.',
    })


@task(ignore_result=True)
def serve(app_name, uuid):
    client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
    app_info = client.private.app_info(app_name)

    chain(
        generate_config.s((app_info, uuid)),
        reload_nginx.s(),
        end.s()
    ).apply_async()


@task(ignore_result=True)
def unserve(app_name, uuid):
    client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
    app_info = client.private.app_info(app_name)

    chain(
        delete_config.s((app_info, uuid)),
        reload_nginx.s(),
        end.s()
    ).apply_async()
