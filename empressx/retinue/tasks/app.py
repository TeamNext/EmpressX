import os
import xmlrpclib

from copy import copy
from celery import chain, task
from django.template.loader import render_to_string

from empressx.retinue.conf import settings
from empressx.retinue.utils import localcommand, virtualenvcommand


@task
def delete_config(app_name):
    conf_home = settings.RETINUE_VASSAL_HOME
    localcommand("rm -f %(conf_home)s/%(app_name)s.ini" % locals())
    return app_name


@task
def provide_virtualenv(app_name):
    client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
    app_info = client.app_info(app_name)

    virtualenv = app_info.get('virtualenv', app_name)

    # mkvirtualenv if not exist
    if virtualenv not in virtualenvcommand('lsvirtualenv -b').splitlines():
        virtualenvcommand('mkvirtualenv %s' % virtualenv)

    project_home = '%s/%s' % (settings.RETINUE_APP_HOME, app_name)
    # mkdir project_home if not exist
    localcommand('mkdir -p %s' % project_home)

    virtualenvcommand('workon %s && cd %s && setvirtualenvproject $VIRTUAL_ENV `pwd`' % (virtualenv, project_home))

    return app_name


@task
def pull_source_code(app_name):
    client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
    app_info = client.app_info(app_name)

    project_home = '%s/%s' % (settings.RETINUE_APP_HOME, app_name)

    vcs_path = app_info.get('vcs', {}).get('path')
    username = app_info.get('vcs', {}).get('username')
    password = app_info.get('vcs', {}).get('password')

    localcommand("""
if [ -d %(project_home)s/.svn ]
then
    svn cleanup --username=%(username)s --password=%(password)s
    svn update --username=%(username)s --password=%(password)s
else
    cd %(project_home)s
    svn checkout %(vcs_path)s/ . --non-interactive --no-auth-cache --username=%(username)s --password=%(password)s
fi
    """ % locals())

    return app_name


@task
def install_requirements(app_name):
    client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
    app_info = client.app_info(app_name)

    virtualenv = app_info.get('virtualenv', app_name)
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

    return app_name


@task
def render_vassal_config(app_name):
    client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
    app_info = client.app_info(app_name)

    context = copy(app_info)
    context.update({
        'RETINUE_HOME': settings.RETINUE_HOME,
        'RETINUE_WORKON_HOME': settings.RETINUE_WORKON_HOME,
        'RETINUE_APP_HOME': settings.RETINUE_APP_HOME,
    })

    rendered = render_to_string('empressx/retinue/uwsgi.ini', context)

    with open('%s/%s.ini' % (settings.RETINUE_VASSAL_HOME, app_name), 'w') as f:
        f.write(rendered)

    return app_name


@task(ignore_result=True)
def update(app_name, uuid):
    chain(provide_virtualenv.s(app_name),
          pull_source_code.s(),
          install_requirements.s()).apply_async()


@task(ignore_result=True)
def serve(app_name, uuid):
    chain(provide_virtualenv.s(app_name),
          pull_source_code.s(),
          install_requirements.s(),
          render_vassal_config.s()).apply_async()


@task(ignore_result=True)
def unserve(app_name, uuid):
    chain(delete_config.s(app_name)).apply_async()
