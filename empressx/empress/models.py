# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone


class Application(models.Model):

    name = models.CharField(unique=True, max_length=100, )
    alias = models.CharField(blank=True, max_length=100, default='')
    svn_path = models.CharField(max_length=200, )
    project_path = models.CharField(blank=True, max_length=100,  default='') #${retinue_app_dir}/${app_code}/${project_path}(只需填相对路径)
    wsgi_handler = models.CharField(max_length=100, choices=(
        ('django.core.handlers.wsgi:WSGIHandler()', 'django<=1.3'),
        ('django.core.wsgi:get_wsgi_application()', 'django>=1.4'),
    ))
    virtual_env = models.CharField(max_length=100, blank=True) # 用户可以自定义环境
    # requirements = models.TextField() # requirements改存到app文件中

    def __unicode__(self):
        if self.alias:
            return unicode("{}({})".format(self.alias,
                                           self.name))
        else:
            return self.name

    def output_app_info(self):
        rels = Relationship.objects.filter(application=self, is_active=True)
        hosts = [rel.server.ip for rel in rels]
        envs = {env.key:env.value for env in Environment.objects.filter(application=self)}
        return  {
                    'app_name': self.name,
                    'envs': self.envs,
                    'hosts': self.hosts,
                    'virtual_env': self.virtual_env,
                    'project_path' : self.project_path,
                    'vcs':{
                        'path': self.svn_path, # svn
                        'username': None, # optional
                        'password': None, # optional
                    },
                    #'requirements': 'requirements.txt', (default)
                    'wsgi_handler' : self.wsgi_handler,
                }


class Server(models.Model):
    '''根据心跳动态调整is_active， 然后动态切换relationship'''
    ip = models.CharField(unique=True, max_length=100, )
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=30, choices=(
        ('WebSvr', 'web'),
        ('AppSvr', 'app'),
    ))  #todo: 换成role-group
    url = models.URLField(unique=True)

    def __unicode__(self):
        return unicode("{}({})".format(self.category,
                                       self.ip))


class Environment(models.Model):

    application = models.ForeignKey(Application)
    key = models.CharField(max_length=100, )
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
        ('app.update', u'App服务器初始化/更新App环境'),
        ('app.serve', u'App服务器启动一个App'),
        ('app.unserve', u'App服务器停止一个App'),
        ('web.serve', u'Web服务器路由一个app'),
        ('web.unserve', u'Web服务器停止路由一个app'),
    )

    uuid = models.CharField(max_length=64, unique=True, editable=False)
    retinue = models.ForeignKey(Server)  # 执行命令的随从
    app = models.ForeignKey(Application)
    command = models.CharField(choices=COMMAND_CHOICE, max_length=30, )
    status = models.CharField(max_length=30, choices=(
        ('sent', u'命令已下达，等待随从报告'),
        ('failed', u'随从报告任务失败'),
        ('complete', u'随从报告任务成功'),
    ), default='sent')
    callback = models.TextField(null=True) # 随从返回报告的内容

    sent_time = models.DateTimeField(default=timezone.now())
    callback_time = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode("[{}] {} --> {}".format(self.command,
                                           self.app.name,
                                           self.status))