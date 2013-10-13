# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone


class Application(models.Model):

    name = models.CharField(unique=True)
    alias = models.CharField(blank=True, default='')
    svn_path = models.CharField()
    project_path = models.CharField(blank=True, default='') #${retinue_app_dir}/${app_code}/${project_path}(只需填相对路径)
    wsgi_handler = models.CharField(choices=(
        ('django.core.handlers.wsgi:WSGIHandler()', 'django<=1.3'),
        ('django.core.wsgi:get_wsgi_application()', 'django>=1.4'),
    ))
    # requirements = models.TextField() # requirements改存到app文件中

    def __unicode__(self):
        if self.alias:
            return unicode("{}({})".format(self.alias,
                                           self.name))
        else:
            return self.name

    def output_app_config(self):
        return  {
                    'svn_path': self.svn_path,
                    'project_path' : self.project_path,
                    'wsgi_handler' : self.wsgi_handler,
                }


class Server(models.Model):
    '''根据心跳动态调整is_active， 然后动态切换relationship'''
    ip = models.CharField(unique=True)
    is_active = models.BooleanField(default=True)
    category = models.CharField(choices=(
        ('WebSvr', 'web'),
        ('AppSvr', 'app'),
    ))  #todo: 换成role-group
    url = models.URLField(unique=True)


class Environment(models.Model):

    application = models.ForeignKey(Application)
    key = models.CharField()
    value = models.TextField()


class Relationship(models.Model):
    '''App部署在某台机器的关系'''
    application = models.ForeignKey(Application)
    server = models.ForeignKey(Server)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now())
    date_deprecated = models.DateTimeField(null=True)

    def __unicode__(self):
        if self.is_active:
            state = 'ACTIVE'
        else:
            state = 'INACTIVE'

        return unicode("[{}] {}@{}".format(state,
                                           self.application,
                                           self.server))


class EmpressMission(models.Model):
    '''女皇对随从的命令记录'''
    COMMAND_CHOICE = (
        ('appsvr_init_app', u'App服务器初始化App环境'),
        ('appsvr_start_serve_app', u'App服务器启动一个App'),
        ('appsvr_stop_serve_app', u'App服务器停止一个App'),
        ('websvr_reload', u'Web服务器刷新路由配置'),
    )

    retinue = models.ForeignKey(Server)  # 执行命令的随从
    app = models.ForeignKey(Application)
    command = models.CharField(choices=COMMAND_CHOICE)
    status = models.CharField(choices=(
        ('sent', u'命令已下达，等待随从报告'),
        ('failed', u'随从报告任务失败'),
        ('complete', u'随从报告任务成功'),
    ), default='sent')
    callback = models.TextField(null=True) # 随从返回报告的内容

    sent_time = models.DateTimeField(default=timezone.now())
    callback_time = models.DateTimeField(null=True)
