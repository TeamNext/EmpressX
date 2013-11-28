# -*- coding: utf-8 -*-
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


def get_uuid():
    return str(uuid.uuid4())


class VirtualEnv(models.Model):

    name = models.SlugField(max_length=255, unique=True)
    is_public = models.BooleanField(default=False)

    def __unicode__(self):
        category = 'PRIVATE'
        if self.is_public:
            category = 'PUBLIC'

        return unicode("[{}] {}".format(category,
                                        self.name))


class Application(models.Model):

    name = models.CharField(unique=True, max_length=255)
    alias = models.CharField(max_length=255, default='', blank=True)
    is_active = models.BooleanField(default=True)

    virtualenv = models.ForeignKey(VirtualEnv, null=True, blank=True)

    # vcs settings
    vcs = models.CharField(max_length=255, choices=(
        ('Subversion', 'Subversion'),
    ), default='Subversion')
    vcs_path = models.CharField(max_length=255, default='', blank=True)
    vcs_username = models.CharField(max_length=255, default='svn_t', blank=True)
    vcs_password = models.CharField(max_length=255, default='71A1Wt05Yj', blank=True)

    min_worker_num = models.PositiveSmallIntegerField(default=1)
    max_worker_num = models.PositiveSmallIntegerField(default=4)

    project_path = models.CharField(max_length=255, default='', blank=True)
    requirements = models.CharField(max_length=255, default='', blank=True)
    wsgi_handler = models.CharField(max_length=255, choices=(
        ('django.core.handlers.wsgi:WSGIHandler()', 'django<=1.3'),
        ('django.core.wsgi:get_wsgi_application()', 'django>=1.4'),
    ), default='django.core.handlers.wsgi:WSGIHandler()')

    use_celery = models.BooleanField(default=False)
    use_celery_beat = models.BooleanField(default=False)
    celery_stop_wait_secs = models.PositiveIntegerField(default=60)

    min_celery_worker_num = models.PositiveSmallIntegerField(default=1)
    max_celery_worker_num = models.PositiveSmallIntegerField(default=4)

    def __unicode__(self):
        if self.alias:
            return unicode("{}({})".format(self.alias,
                                           self.name))
        else:
            return self.name


class EnvironmentVariable(models.Model):

    application = models.ForeignKey(Application)
    name = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        unique_together = ('application', 'name')

    def __unicode__(self):
        return unicode('[{}] {}'.format(self.application,
                                        self.name))


class Server(models.Model):

    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField(default=80)
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=255, choices=(
        ('web', 'WebSvr'),
        ('app', 'AppSvr'),
    ))
    affinity = models.PositiveSmallIntegerField(null=True, blank=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    applications = models.ManyToManyField(Application, through='HostingShip')

    class Meta:
        unique_together = ('ip_address', 'port', 'category')

    def __unicode__(self):
        return unicode("[{}] {}:{}".format(self.category,
                                           self.ip_address,
                                           self.port))


class HostingShip(models.Model):

    application = models.ForeignKey(Application)
    server = models.ForeignKey(Server)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_deprecated = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        if self.is_active:
            state = 'ACTIVE'
        else:
            state = 'INACTIVE'

        return unicode("[{}] {}@{}".format(state,
                                           self.application.name,
                                           self.server.ip_address))


class Task(models.Model):

    id = models.CharField(max_length=255, primary_key=True, default=get_uuid)
    app_name = models.SlugField(max_length=255)
    action = models.CharField(max_length=255, choices=(
        ('serve', 'serve'),
        ('unserve', 'unserve'),
    ))
    state = models.CharField(max_length=255, choices=(
        ('PENDING', 'PENDING'),
        ('STARTED', 'STARTED'),
        ('SUCCESS', 'SUCCESS'),
        ('FAILURE', 'FAILURE'),
    ), default='PENDING')
    data = models.TextField(default='')
    ex_data = models.TextField(default='')
    date_created = models.DateTimeField(default=timezone.now)
    date_archived = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "[{}] {}".format(self.action, self.app_name)


class EmpressMission(models.Model):

    id = models.CharField(max_length=255, primary_key=True, default=get_uuid)
    task = models.ForeignKey(Task)
    action = models.CharField(max_length=255, choices=(
        ('app.serve', 'app.serve'),
        ('app.unserve', 'app.unserve'),
        ('app.reserve', 'app.reserve'),
        ('web.serve', 'web.serve'),
        ('web.unserve', 'web.unserve'),
    ))
    retinue = models.ForeignKey(Server)
    state = models.CharField(max_length=255, choices=(
        ('PENDING', 'PENDING'),
        ('STARTED', 'STARTED'),
        ('SUCCESS', 'SUCCESS'),
        ('FAILURE', 'FAILURE'),
    ), default='PENDING')
    data = models.TextField(default='')
    ex_data = models.TextField(default='')
    date_created = models.DateTimeField(default=timezone.now)
    date_archived = models.DateTimeField(null=True, blank=True)
