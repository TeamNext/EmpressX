import logging

from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

dispatcher = SimpleXMLRPCDispatcher()

logger = logging.getLogger('django.request')


@csrf_exempt
def xmlrpc_handler(request, service=None):

    if request.method == "POST":
        # logger.debug('%s\n\n\n', request.body)
        response = HttpResponse(mimetype="application/xml")
        response.write(dispatcher._marshaled_dispatch(request.body))
        response['Content-length'] = str(len(response.content))
        return response
    else:
        return HttpResponseNotAllowed(['POST'])
