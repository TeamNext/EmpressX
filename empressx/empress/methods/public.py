from empressx import states
from empressx.empress.models import Task


def serve(app_name):
    task = Task(app_name=app_name, action='serve')
    task.save()
    return True, task.id


def unserve(app_name):
    task = Task(app_name=app_name, action='unserve')
    task.save()
    return True, task.id


def status(task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return False, "Invalid 'task_id'."
    else:
        if task.state == states.FAILURE:
            qs = task.empressmission_set.filter(state=states.FAILURE)
            errors = []
            for mission in qs:
                errors.append(mission.ex_data)
            l = []
            for i, msg in enumerate(errors):
                title = "ERROR: #%d ********\r\n" % i
                l.append(title)
                l.append(msg)

            return True, {
                'state': task.state,
                'data': task.data,
                'ex_data': '\r\n'.join(l)
            }
        else:
            return True, {
                'state': task.state,
                'data': task.data,
            }
