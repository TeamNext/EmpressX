import os

from celery import chain, task
from django.template.loader import render_to_string

from empressx.retinue.conf import settings
from empressx.retinue.utils import localcommand, virtualenvcommand


@task
def provide_virtualenv(app_name):
    # mkvirtualenv if not exist
    if app_name not in virtualenvcommand('lsvirtualenv -b').splitlines():
        virtualenvcommand('mkvirtualenv %s' % app_name)

    project_home = '%s/sites/%s' % (settings.RETINUE_HOME, app_name)
    # mkdir project_home if not exist
    localcommand('mkdir -p %s' % project_home)

    virtualenvcommand('workon %s && cd %s && setvirtualenvproject $VIRTUAL_ENV `pwd`' % (app_name, project_home))

    return app_name


@task
def pull_source_code(app_name):
    project_home = '%s/sites/%s' % (settings.RETINUE_HOME, app_name)

    username = settings.RETINUE_SVN_USERNAME
    password = settings.RETINUE_SVN_PASSWORD

    svn_base_path = settings.RETINUE_SVN_BASE_PATH

    localcommand("""
if [ -d %(project_home)s/.svn ]
then
    svn cleanup --username=%(username)s --password=%(password)s
    svn update --username=%(username)s --password=%(password)s
else
    cd %(project_home)s
    svn checkout %(svn_base_path)s/%(app_name)s/ . --non-interactive --no-auth-cache --username=%(username)s --password=%(password)s
fi
    """ % locals())

    return app_name


@task
def install_requirements(app_name):
    project_home = '%s/sites/%s' % (settings.RETINUE_HOME, app_name)

    virtualenvcommand("""
cd %s
if [ -f requirements.txt ]
then
    pip install --upgrade -r requirements.txt
fi
    """ % project_home)

    return app_name


@task
def render_vassal_config(app_name):
    context = {
        'RETINUE_HOME': settings.RETINUE_HOME,
        'WORKON_HOME': os.environ.get('WORKON_HOME', '/Users/sveinchen/.virtualenvs'),
        'wsgi_handler': 'django.core.handlers.wsgi:WSGIHandler()',
        'envs': {
            'DJANGO_CONF_MODULE': 'conf.testing',
            'DJANGO_SETTINGS_MODULE': 'settings',
            'PYTHON_EGG_CACHE': '/Users/sveinchen/.python-eggs'
        },
        'app_name': app_name,
    }

    rendered = render_to_string('empressx/retinue/uwsgi.ini', context)

    with open('%s/etc/vassals/%s.ini' % (settings.RETINUE_HOME, app_name), 'w') as f:
        f.write(rendered)

    return app_name


@task(ignore_result=True)
def update(app_name, revision=None):
    chain(provide_virtualenv.s(app_name),
          pull_source_code.s(),
          install_requirements.s()).apply_async()


@task(ignore_result=True)
def serve(app_name, revision=None):
    chain(provide_virtualenv.s(app_name),
          pull_source_code.s(),
          install_requirements.s(),
          render_vassal_config.s()).apply_async()


@task(ignore_result=True)
def unserve(app_name, revision=None):
    chain(provide_virtualenv.s(app_name),
          pull_source_code.s(),
          install_requirements.s(),
          render_vassal_config.s()).apply_async()
