from django.db import models
from django.utils import timezone


class Application(models.Model):

    name = models.CharField(unique=True)
    alias = models.CharField(blank=True, default='')
    svn_path = models.CharField()
    project_path = models.CharField()
    wsgi_handler = models.CharField()
    requirements = models.TextField()

    def __unicode__(self):
        if self.alias:
            return unicode("{}({})".format(self.alias,
                                           self.name))
        else:
            return self.name


class Server(models.Model):

    host_name = models.CharField(unique=True)
    is_active = models.BooleanField(default=True)
    category = models.CharField(choices=(
        ('WebSvr', 'web'),
        ('AppSvr', 'app'),
    ))
    url = models.URLField(unique=True)


class Environment(models.Model):

    application = models.ForeignKey(Application)
    key = models.CharField()
    value = models.TextField()


class Relationship(models.Model):

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
