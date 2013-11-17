# -*- coding: utf-8 -*-
from django.db.models import signals
from django.dispatch import receiver

from empressx.empress import tasks
from empressx.empress.models import Application, HostingShip, Server, Task, EmpressMission


@receiver(signals.post_save, sender=Application)
def app_post_save_handler(sender, instance, created, **kwargs):
    if created:
        if not instance.vcs_path:
            vcs_path = 'svn://10.130.131.232:8080/apps/{}'.format(instance.name)
            Application.objects.filter(pk=instance.pk) \
                               .update(vcs_path=vcs_path)

        qs = Server.objects.filter(category='app')
        server_count = qs.count()
        if server_count in (1, 2):
            for server in qs:
                HostingShip(application=instance,
                            server=server).save()
        elif server_count > 2:
            server_dict = {}
            for server in qs:
                server_dict[server] = server.applications.count()
            hosting_counts = set(server_dict.values())
            min_values = []
            if len(hosting_counts) == 1:
                min_values.append(hosting_counts.pop())
            else:
                min_value = min(hosting_counts)
                min_values.append(min_value)
                hosting_counts.remove(min_value)
                min_value = min(hosting_counts)
                min_values.append(min_value)

            times = 0
            for server, hosting_count in server_dict.iteritems():
                if hosting_count in min_values:
                    HostingShip(application=instance,
                                server=server).save()
                    times += 1
                    if times >= 2:
                        break


@receiver(signals.post_save, sender=Server)
def server_post_save_handler(sender, instance, created, **kwargs):
    if created:
        # TODO
        pass


@receiver(signals.post_save, sender=Task)
def task_post_save_handler(sender, instance, created, **kwargs):
    if created:
        try:
            app = Application.objects.get(name=instance.app_name)
        except Application.DoesNotExist:
            app = Application(name=instance.app_name)
            app.save()

        for app_retinue in app.server_set.all():
            EmpressMission(task=instance,
                           action='app.serve',
                           retinue=app_retinue).save()

        for web_retinue in Server.objects.filter(category='web'):
            EmpressMission(task=instance,
                           action='web.serve',
                           retinue=web_retinue).save()


@receiver(signals.post_save, sender=EmpressMission)
def mission_post_save_handler(sender, instance, created, **kwargs):
    if created:
        tasks.xmlrpc_client.apply_async(args=[instance.id])
    else:
        pass
