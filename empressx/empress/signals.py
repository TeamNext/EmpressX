# -*- coding: utf-8 -*-
"""
empress.signals
==================

django Signals
-------
"""
import requests

from django.db.models import signals
from django.dispatch import receiver

from empress.models import Application, Relationship, Server, Environment, EmpressMission

#tips: 所有后续需要改写webserver路由配置的操作，都会由celery异步触发
#tips: 所有对随从服务的请求都会触发一个事件记录，并会等待随从服务的完成回调，然后做后续操作

#todo: Environment的传递
#todo: 异常处理
#todo: 将来新增一台Server也需要触发一系列操作


@receiver(signals.post_save, sender=Application)
def app_post_save_handler(sender, instance, created, **kwargs):
    if created:
        # 通知所有App服务器，初始化app运行
        for appsvr in Server.objects.filter(category='AppSvr', is_active=True):
            EmpressMission(retinue=appsvr,app=instance,command='appsvr_init_app').save()
        

@receiver(signals.post_save, sender=Relationship)
def rel_post_save_handler(sender, instance, created, **kwargs):
    if created:
        if instance.is_active:
            # 拉起app服务进程(也需要根据最新代码重新init)
            EmpressMission(retinue=instance.server,app=instance.application,command='appsvr_start_serve_app').save()
    else:
        # 根据is_active情况，停止app服务进程
        if not instance.is_active:
            EmpressMission(retinue=instance.server,app=instance.application,command='appsvr_stop_serve_app').save()


@receiver(signals.post_save, sender=EmpressMission)
def mission_post_save_handler(sender, instance, created, **kwargs):
    if created:
        assert instance.command in dict(EmpressMission.COMMAND_CHOICE)

        #执行一次女王的任务
        if instance.command=='appsvr_init_app':
            url = '%sretinue/appsvr_init_app/' % instance.retinue.url
            data = {
                'svn_path': instance.app.svn_path,
                'project_path' = instance.app.project_path,
                'wsgi_handler' = instance.app.wsgi_handler,
            }

        elif instance.command=='appsvr_start_serve_app':
            url = '%sretinue/appsvr_start_serve_app/' % instance.retinue.url
            data = {
                'svn_path': instance.app.svn_path,
                'project_path' : instance.app.project_path,
                'wsgi_handler' : instance.app.wsgi_handler,
            }

        elif instance.command=='appsvr_stop_serve_app':
            url = '%sretinue/appsvr_stop_serve_app/' % instance.retinue.url
            data = {
                'project_path' : instance.app.project_path,
                'wsgi_handler' : instance.app.wsgi_handler,
            }
        elif instance.command=='websvr_reload':
            # 获取每台app_svr负载的app清单
            server_list = []
            for appsvr in Server.objects.filter(category='AppSvr', is_active=True):
                data = {'host_name': appsvr.host_name, 'host_apps':[]}
                for rel in Relationship.objects.filter(server=appsvr, is_active=True):
                    data['host_apps'].append(rel.Application.name) #可能需要给wsgi_handler
                server_list.append(data)

            url = '%sretinue/websvr_reload/' % instance.retinue.url
            data = {
                'server_list': json.dumps(server_list)
            }

        data['mission_id'] = mission.id
        response = requests.post(url, data=data)
        assert httplib.OK == response.status_code
