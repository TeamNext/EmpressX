from __future__ import absolute_import

from celery.signals import worker_init


@worker_init.connect
def worker_init_handler(**kwargs):
    # TODO
    pass
