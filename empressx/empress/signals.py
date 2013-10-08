# -*- coding: utf-8 -*-
"""
empress.signals
==================

django Signals
-------
"""
import requests
import xmlrpclib

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

        retinue_api = xmlrpclib.ServerProxy(instance.retinue.url, allow_none=True, use_datetime=True)
        data = {'mission_id':mission.id}

        try:
            #执行一次女王的任务
            if instance.command=='appsvr_init_app':
                data.update(instance.app.output_app_config())
                retinue_api.appsvr_init_app(**data)

            elif instance.command=='appsvr_start_serve_app':
                data.update(instance.app.output_app_config())
                retinue_api.appsvr_start_serve_app(**data)

            elif instance.command=='appsvr_stop_serve_app':
                data.update(instance.app.output_app_config())
                retinue_api.appsvr_stop_serve_app(**data)

            elif instance.command=='websvr_reload':
                # 获取每台app_svr负载的app清单
                svr_list = []
                for appsvr in Server.objects.filter(category='AppSvr', is_active=True):
                    svr_data = {'ip': appsvr.ip, 'host_apps':[]}
                    for rel in Relationship.objects.filter(server=appsvr, is_active=True):
                        svr_data['host_apps'].append(rel.Application.name) #可能需要给wsgi_handler
                    svr_list.append(svr_data)

                data.update{
                    'server_list': json.dumps(svr_list)
                }
                retinue_api.websvr_reload(**data)
        except xmlrpclib.Fault as err::
            return (False, u"调用错误: %s" % err.faultString)

