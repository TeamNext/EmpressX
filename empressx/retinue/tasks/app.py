import os
import time
import traceback
import xmlrpclib

from copy import copy
from celery import chain, task
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils import timezone
from functools import wraps

from empressx import states
from empressx.retinue.conf import settings
from empressx.retinue.utils import localcommand, virtualenvcommand


def task_tracker(func):
    @wraps(func)
    def wrapper(target):
        if target:
            app_info, uuid = target
            rpc_client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)

            rpc_client.private.callback({
                'uuid': uuid,
                'state': states.STARTED,
                'data': func.__name__,
            })
            try:
                result = func(target)
            except:
                rpc_client.private.callback({
                    'uuid': uuid,
                    'state': states.FAILURE,
                    'data': func.__name__,
                    'ex_data': traceback.format_exc(),
                })
            else:
                return result

    return wrapper


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

@task
@task_tracker
def delete_config(app_name):
    conf_home = settings.RETINUE_VASSAL_HOME
    localcommand("rm -f %(conf_home)s/%(app_name)s.ini" % locals())
    return app_name


@task
@task_tracker
def provide_virtualenv(target):
    app_info, uuid = target
    app_name = app_info['app_name']
    virtualenv = app_info.get('virtualenv', app_name)

    # mkvirtualenv if not exist
    if virtualenv not in virtualenvcommand('lsvirtualenv -b').splitlines():
        virtualenvcommand('mkvirtualenv %s' % virtualenv)

    project_home = '%s/%s' % (settings.RETINUE_APP_HOME, app_name)
    # mkdir project_home if not exist
    if not os.path.exists(project_home):
        os.makedirs(project_home)

    if virtualenv == app_name:
        virtualenvcommand('workon %s && cd %s && setvirtualenvproject $VIRTUAL_ENV `pwd`' % (virtualenv, project_home))

    return target


@task
@task_tracker
def pull_source_code(target):
    app_info, uuid = target
    app_name = app_info['app_name']

    project_home = '%s/%s' % (settings.RETINUE_APP_HOME, app_name)

    vcs_type = app_info.get('vcs', {}).get('type')
    vcs_path = app_info.get('vcs', {}).get('path')
    vcs_username = app_info.get('vcs', {}).get('username')
    vcs_password = app_info.get('vcs', {}).get('password')

    cmd = """
if [ -d %(project_home)s/.svn ]
then
    svn cleanup --username=%(vcs_username)s --password=%(vcs_password)s
    svn update --username=%(vcs_username)s --password=%(vcs_password)s
else
    cd %(project_home)s
    svn checkout %(vcs_path)s/ . --non-interactive --no-auth-cache --username=%(vcs_username)s --password=%(vcs_password)s
fi
    """ % locals()

    print cmd

    localcommand(cmd)

    return target


@task
@task_tracker
def install_requirements(target):
    app_info, uuid = target
    app_name = app_info['app_name']
    virtualenv = app_info.get('virtualenv', app_name)

    if virtualenv == app_name:
        requirements = app_info.get('requirements', 'requirements.txt')

        project_home = '%s/%s' % (settings.RETINUE_APP_HOME, app_name)

        virtualenvcommand("""
workon %(virtualenv)s
cd %(project_home)s
if [ -f %(requirements)s ]
then
    pip install --upgrade -r %(requirements)s
fi
        """ % locals())

    return target


@task
@task_tracker
def syncdb_and_migrate(target):
    app_info, uuid = target
    app_name = app_info['app_name']
    virtualenv = app_info.get('virtualenv', app_name)

    project_home = '%s/%s' % (settings.RETINUE_APP_HOME, app_name)

    virtualenvcommand("""
workon %(virtualenv)s
cd %(project_home)s
python manage.py syncdb --noinput
python manage.py migrate --noinput
    """ % locals())

    return target


@task
@task_tracker
def render_uwsgi_config(target):
    app_info, uuid = target
    app_name = app_info['app_name']

    context = copy(app_info)
    context.update({
        'RETINUE_HOME': settings.RETINUE_HOME,
        'RETINUE_WORKON_HOME': settings.RETINUE_WORKON_HOME,
        'RETINUE_APP_HOME': settings.RETINUE_APP_HOME,
    })

    rendered = render_to_string('empressx/retinue/uwsgi.ini', context)

    with open('%s/%s.ini' % (settings.RETINUE_VASSAL_HOME, app_name), 'w') as f:
        f.write(rendered)

    return target


@task
@task_tracker
def render_nginx_config(target):
    app_info, uuid = target
    app_name = app_info['app_name']

    context = copy(app_info)
    context.update({
        'project_home': '%s/%s' % (settings.RETINUE_APP_HOME, app_name),
    })

    rendered = render_to_string('empressx/retinue/staticfile.conf', context)

    with open('%s/%s.conf' % (settings.RETINUE_NGINX_STATICFILE_HOME, app_name), 'w') as f:
        f.write(rendered)

    return target


@task
@task_tracker
def reload_nginx(target):
    cache.set('nginx_last_reload_request', time.mktime(timezone.now().timetuple()))
    _reload_nginx.apply_async(countdown=30)
    return target


@task(ignore_result=True)
def _reload_nginx():
    last_reload_request = cache.get('nginx_last_reload_request')
    now = time.mktime(timezone.now().timetuple())
    if now - last_reload_request >= 30:
        nginx_path = settings.RETINUE_NGINX_PATH
        conf = settings.RETINUE_NGINX_CONF if settings.RETINUE_NGINX_CONF else 'conf/nginx.conf'
        localcommand("%(nginx_path)s -s reload -c %(conf)s" % locals())


@task(ignore_result=True)
def reserve(app_name, uuid):
    chain(provide_virtualenv.s(app_name),
          pull_source_code.s(),
          install_requirements.s()).apply_async()


@task(ignore_result=True)
def serve(app_name, uuid):
    client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
    app_info = client.private.app_info(app_name)

    chain(
        provide_virtualenv.s((app_info, uuid)),
        pull_source_code.s(),
        install_requirements.s(),
        syncdb_and_migrate.s(),
        render_uwsgi_config.s(),
        render_nginx_config.s(),
        reload_nginx.s(),
        end.s(),
    ).apply_async()


@task(ignore_result=True)
def unserve(app_name, uuid):
    chain(delete_config.s(app_name)).apply_async()
