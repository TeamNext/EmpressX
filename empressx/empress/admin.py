# coding=utf-8

from django.contrib import admin

from empressx.empress.models import Application, HostingShip, Server, Task, EmpressMission


class ApplicationAdmin(admin.ModelAdmin):

    list_display = ['name', 'is_active', 'min_worker_num', 'max_worker_num', 'virtualenv', 'use_celery', 'use_celery_beat', 'max_celery_worker_num']
    list_filter = ['is_active', 'use_celery', 'use_celery_beat']
    search_fields = ['name']

    ordering = ['name']

    fieldsets = (
        (None, {'fields': ['name', 'alias', 'is_active']}),
        ('Basic', {'fields': ['virtualenv', 'project_path', 'requirements', 'wsgi_handler']}),
        ('Worker', {'fields': ['min_worker_num', 'max_worker_num']}),
        ('VCS', {'fields': ['vcs', 'vcs_path', 'vcs_username', 'vcs_password']}),
        ('Celery', {'fields': ['use_celery', 'use_celery_beat', 'max_celery_worker_num', 'celery_stop_wait_secs']}),
    )


class TaskAdmin(admin.ModelAdmin):

    list_display = ('app_name', 'state', 'date_created', 'date_archived')
    list_filter = ['state']
    ordering = ['-date_created']
    readonly_fields = ['date_created', 'date_archived']
    search_fields = ['app_name']


class EmpressMissionAdmin(admin.ModelAdmin):

    list_display = ['task', 'action', 'retinue', 'state', 'date_created', 'date_archived']
    list_filter = ['state']
    ordering = ['-date_created']


class ServerAdmin(admin.ModelAdmin):

    list_display = ['ip_address', 'port', 'category', 'affinity', 'identifier_code', 'is_active', 'last_heartbeat']
    ordering = ['ip_address']
    list_filter = ['category']


class HostingShipAdmin(admin.ModelAdmin):

    list_display = ['application', 'server', 'is_active', 'date_created', 'date_deprecated']
    list_filter = ['is_active', 'server']
    ordering = ['-date_created', 'application__name']


admin.site.register(Application, ApplicationAdmin)
admin.site.register(HostingShip, HostingShipAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(EmpressMission, EmpressMissionAdmin)

