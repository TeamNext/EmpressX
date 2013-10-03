# Create your views here.
import json
from django.http import HttpResponse

def get_server_app_list(request):
    '''获取每台app_svr负载的app清单, 用于webserver刷新路由配置时使用'''
    server_list = []
    for appsvr in Server.objects.filter(category='AppSvr'):
        data = {'host_name': appsvr.host_name, 'host_apps':[]}
        for rel in Relationship.objects.filter(server=appsvr, is_active=True):
    		data['host_apps'].append(rel.Application.name) #可能需要给wsgi_handler
    	server_list.append(data)
	return HttpResponse(json.dumps(server_list))
