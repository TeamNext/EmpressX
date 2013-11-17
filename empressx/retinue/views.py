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


from empressx.retinue.methods import app, web
dispatcher.register_function(app.serve, 'app.serve')
dispatcher.register_function(app.unserve, 'app.unserve')
dispatcher.register_function(app.reserve, 'app.reserve')
dispatcher.register_function(web.serve, 'web.serve')
dispatcher.register_function(web.unserve, 'web.unserve')
