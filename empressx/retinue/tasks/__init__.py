import xmlrpclib

from celery import task
from empressx.retinue.conf import settings

from .app import *
from .web import *


@task(ignore_result=True)
def heartbeat():
    identifier_code = getattr(settings, 'RETINUE_IDENTIFIER_CODE').strip()
    if identifier_code:
        rpc_client = xmlrpclib.Server(settings.EMPRESS_SERVICE_URL)
        rpc_client.private.heartbeat(identifier_code)