# Create your views here.
import json
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from empress.models import EmpressMission

dispatcher = SimpleXMLRPCDispatcher()


@csrf_exempt
def xmlrpc_handler(request):
    '''用于随从服务器回调的xmlrpc服务'''
    if request.method == "POST":
        # logger.debug('%s\n\n\n', request.body)
        response = HttpResponse(mimetype="application/xml")
        response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
        response['Content-length'] = str(len(response.content))
        return response
    else:
        raise Http404(u'只支持POST请求')


def mission_report(mission_id, is_complete, data):
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

dispatcher.register_function(mission_report, 'mission_report')
