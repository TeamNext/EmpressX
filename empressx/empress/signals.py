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

from empress.models import Application, Relationship, Server, Environment

#tips: 所有后续需要改写webserver路由配置的操作，都会由celery异步触发
#todo: Environment的传递
#todo: 异常处理
#todo: 将来新增一台Server也需要触发一系列操作


@receiver(signals.post_save, sender=Application)
def app_post_save_handler(sender, instance, created, **kwargs):
    if created:
        # 通知所有App服务器，初始化app运行
        for appsvr in Server.objects.filter(category='AppSvr'):
            init_app(appsvr, instance)
        

@receiver(signals.post_save, sender=Relationship)
def rel_post_save_handler(sender, instance, created, **kwargs):
    if created:
        # 拉起app服务进程(也需要根据最新代码重新init)
        start_serve_app(instance.server, instance.application)

    else:
        # 根据is_active情况，停止app服务进程
        stop_serve_app(instance.server, instance.application)


def init_app(appsvr, app):
    '''通知App随从服务器初始化app'''
    url = '%sretinue/init_app/' % appsvr.url
    data = {
        'svn_path': app.svn_path
        'project_path' = app.project_path
        'wsgi_handler' = app.wsgi_handler
        'requirements' = app.requirements
    }
    response = requests.post(url, data=data)
    assert httplib.OK == response.status_code


def start_serve_app(appsvr, app):
    '''通知appsvr拉起app服务进程'''
    url = '%sretinue/start_server_app/' % appsvr.url
    data = {
        'svn_path': app.svn_path
        'project_path' = app.project_path
        'wsgi_handler' = app.wsgi_handler
        'requirements' = app.requirements
    }
    response = requests.post(url, data=data)
    assert httplib.OK == response.status_code



def stop_serve_app(appsvr, app):
    '''通知appsvr停止app服务进程'''
    url = '%sretinue/stop_serve_app/' % appsvr.url
    data = {
        'project_path' = app.project_path
        'wsgi_handler' = app.wsgi_handler
    }
    response = requests.post(url, data=data)
    assert httplib.OK == response.status_code

