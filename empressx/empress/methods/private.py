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
        return {
            'app_name': app.name,
            'virtualenv': app.virtualenv_name,
            'hosts': ['%s:%d' % (server.ip_address, server.port) for server in app.server_set.all()],
            'envs': {
                'DJANGO_CONF_MODULE': 'conf.testing',
                'DJANGO_SETTINGS_MODULE': 'settings',
            },
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
        }


def heartbeat(category):
    pass