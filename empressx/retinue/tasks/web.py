from celery import chain, task

from empressx.retinue.conf import settings
from empressx.retinue.utils import localcommand


@task
def reload_nginx(app_name):
    nginx = settings.ER_WEB_NGINX_PATH
    conf = settings.ER_WEB_NGINX_CONF if settings.ER_WEB_NGINX_CONF else 'conf/nginx.conf'
    localcommand("%(nginx)s -s reload -c %(conf)s" % locals())
    return app_name


@task
def delete_config(app_name):
    conf_home = settings.RETINUE_NGINX_UPSTREAM_HOME
    localcommand("rm -f %(conf_home)s/%(app_name)s.conf" % locals())
    return app_name


@task
def route(app_name):
    # TODO
    pass


@task
def serve(app_name):
    pass


@task
def unserve(app_name):
    pass