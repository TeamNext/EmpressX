import xmlrpclib

from celery import chain, task
from django.utils import timezone
from empressx import states
from empressx.empress.models import Application, Server, Task, EmpressMission, HostingShip


@task(ignore_result=True)
def xmlrpc_client(mission_id):
    try:
        mission = EmpressMission.objects.get(pk=mission_id)
    except EmpressMission.DoesNotExist:
        pass
    else:
        client = xmlrpclib.Server('http://{}:{}/'.format(mission.retinue.ip_address,
                                                         mission.retinue.port))
        method = getattr(client, mission.action)
        try:
            method(mission.task.app_name, mission.id)
        except:
            import traceback
            EmpressMission.objects.filter(pk=mission.pk) \
                                  .update(state=states.FAILURE,
                                          ex_data=traceback.format_exc())

            mission_state_changed.apply_async(args=[mission.id])


@task(ignore_result=True)
def mission_state_changed(mission_id):
    try:
        mission = EmpressMission.objects.get(pk=mission_id)
    except EmpressMission.DoesNotExist:
        pass
    else:
        flag = False

        if mission.state == states.STARTED:
                flag = True
        elif mission.state == states.SUCCESS:
            missions_count = mission.task.empressmission_set.count()
            success_count = mission.task.empressmission_set.filter(state=states.SUCCESS).count()
            if missions_count == success_count:
                flag = True
        elif mission.state == states.FAILURE:
            flag = True

        if flag and states.can_transit(mission.task.state, mission.state):
            kwargs = {
                'state': mission.state,
            }
            if kwargs['state'] in states.ARCHIVED_STATES:
                kwargs['date_archived'] = timezone.now()
            Task.objects.filter(pk=mission.task_id,
                                state=mission.task.state) \
                        .update(**kwargs)


@task(ignore_result=True)
def unserve(task_id):
    pass


@task
def reserve(app_name):
    pass