# coding=utf-8

from django.contrib import admin

from empressx.empress.models import Application, HostingShip, Server, Task, EmpressMission


class ApplicationAdmin(admin.ModelAdmin):

    list_display = ['name', 'alias', 'is_active', 'min_worker_num', 'max_worker_num']


class TaskAdmin(admin.ModelAdmin):

    list_display = ('app_name', 'state', 'date_created', 'date_archived')
    ordering = ['-date_created']
    readonly_fields = ['date_created', 'date_archived']


class EmpressMissionAdmin(admin.ModelAdmin):

    list_display = ['task', 'action', 'retinue', 'state', 'date_created', 'date_archived']
    ordering = ['-date_created']


class ServerAdmin(admin.ModelAdmin):

    list_display = ['ip_address', 'port', 'category', 'is_active', 'last_heartbeat']
    ordering = ['ip_address']
    list_filter = ['category']


class HostingShipAdmin(admin.ModelAdmin):

    list_display = ['application', 'server', 'is_active', 'date_created', 'date_deprecated']

    ordering = ['-date_created', 'application__name']


admin.site.register(Application, ApplicationAdmin)
admin.site.register(HostingShip, HostingShipAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(EmpressMission, EmpressMissionAdmin)

