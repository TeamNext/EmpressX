# -*- coding:utf-8 -*-

# Create your views here.
import json
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from empressx.empress.models import EmpressMission, Application, Server

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


def callback(uuid, result=True, reason=None):
    try:
        mission = EmpressMission.objects.get(uuid=uuid)
    except:
        pass #todo
    else:
        if mission.status == 'sent':
            if mission.command in ('app.serve', 'app.unserve'):
                # 刷新路由配置
                for websvr in Server.objects.filter(category='WebSvr', is_active=True):
                    EmpressMission(retinue=websvr,app=mission.app,command='web.serve').save()
            else:
                pass # 其他任务完成后暂无操作

            # 更新任务信息
            mission.status = 'complete' if result else 'failed'
            mission.callback_time = timezone.now()
            mission.callback = reason
            mission.save()
        else:
            pass # todo: 误报


def app_info(app_name):
    try:
        app = Application.objects.get(name=app_name)
    except:
        pass #todo
    else:
        return app.output_app_info()


dispatcher.register_function(callback, 'callback')
dispatcher.register_function(app_info, 'app_info')
