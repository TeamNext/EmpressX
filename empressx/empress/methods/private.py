import os

from django.utils import timezone
from empressx import states
from empressx.empress import tasks
from empressx.empress.models import EmpressMission, Application, Server


def callback(kwargs):
    try:
        mission = EmpressMission.objects.get(pk=kwargs['uuid'])
    except EmpressMission.DoesNotExist:
        pass
    else:
        _kwargs = {k: v for k, v in kwargs.iteritems() if k in ['data', 'ex_data']}

        state = kwargs['state']
        if state in states.ARCHIVED_STATES:
            _kwargs['date_archived'] = timezone.now()

        if state in states.ALL_STATES:
            rows = EmpressMission.objects.filter(pk=mission.pk,
                                                 state=state) \
                                         .exclude(state__in=states.ARCHIVED_STATES) \
                                         .update(**_kwargs)
            if not rows:
                rows = EmpressMission.objects.filter(pk=mission.pk) \
                                             .exclude(state__in=list(states.ARCHIVED_STATES) + [state]) \
                                             .update(state=state, **_kwargs)

                if rows:
                    tasks.mission_state_changed.apply_async(args=[mission.id])

    return True


def app_info(app_name):
    try:
        app = Application.objects.get(name=app_name)
    except Application.DoesNotExist:
        return {}
    else:
        ret = {
            'app_name': app.name,
            'hosts': ['%s:%d' % (server.ip_address, server.port) for server in app.server_set.all()],
            'vcs': {
                'name': app.vcs,
                'path': app.vcs_path,
                'username': app.vcs_username,
                'password': app.vcs_password,
            },
            'min_worker_num': app.min_worker_num,
            'max_worker_num': app.max_worker_num,
            'project_path': app.project_path,
            'requirements': app.requirements,
            'wsgi_handler': app.wsgi_handler,
            'celery': {
                'enabled': app.use_celery,
                'beat_enabled': app.use_celery_beat,
                'stop_wait_secs': app.celery_stop_wait_secs,
                'max_worker_num': app.max_celery_worker_num,
            },
        }

        if app.virtualenv:
            ret['virtualenv'] = app.virtualenv

        conf_module = os.environ.get('DJANGO_CONF_MODULE', 'conf.testing')
        envs = {
            'DJANGO_CONF_MODULE': conf_module,
            'DJANGO_SETTINGS_MODULE': 'settings',
        }
        if conf_module == 'conf.production':
            envs['CELERY_BROKER'] = 'amqp://ai_logging:ai_logging@10.185.8.141:5672/ai_logging'
        ret['envs'] = envs

        return ret


def virtualenv_info(retinue_id, virtualenv_name=None):
    try:
        server = Server.objects.get(pk=retinue_id)
    except Server.DoesNotExist:
        return []
    else:
        if virtualenv_name:
            qs = server.applications.filter(virtualenv__name=virtualenv_name,
                                            use_celery=True)
        else:
            qs = server.applications.filter(virtualenv__isnull=True,
                                            use_celery=True)

        return map(lambda x: {'name': x.name,
                              'use_celery_beat': x.use_celery_beat,
                              'celery_stop_wait_secs': x.celery_stop_wait_secs,
                              'min_celery_worker_num': x.min_celery_worker_num,
                              'max_celery_worker_num': x.max_celery_worker_num},
                   qs)


def heartbeat(category):
    pass