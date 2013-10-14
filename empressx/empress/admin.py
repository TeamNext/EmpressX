# coding=utf-8

from django.contrib import admin

from empressx.empress.models import Application, Relationship, \
								Server, Environment, EmpressMission


admin.site.register(Application)
admin.site.register(Relationship)
admin.site.register(Server)
admin.site.register(Environment)
admin.site.register(EmpressMission)

