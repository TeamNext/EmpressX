# Create your views here.
import json
from django.http import HttpResponse
from django.utils import timezone
from empress.models import EmpressMission


def mission_report(request, mission_id, is_complete, data):
    try:
        mission = EmpressMission.objects.get(id=mission_id)
    except:
        pass #todo
    else:
        if mission.status == 'sent':
            if mission.command in ('appsvr_start_serve_app', 'appsvr_stop_serve_app'):
                # 刷新路由配置
                for websvr in Server.objects.filter(category='WebSvr', is_active=True):
                    EmpressMission(retinue=websvr,app=mission.app,command='websvr_reload').save()
            else:
                pass # 其他任务完成后暂无操作

            # 更新任务信息
            mission.status = 'complete' if is_complete else 'failed'
            mission.callback_time = timezone.now()
            mission.callback = data
            mission.save()
        else:
            pass # todo: 误报

