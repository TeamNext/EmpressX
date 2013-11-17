# -*- coding:utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

dispatcher = SimpleXMLRPCDispatcher()


@csrf_exempt
def xmlrpc_handler(request):

    if request.method == "POST":
        response = HttpResponse(mimetype="application/xml")
        response.write(dispatcher._marshaled_dispatch(request.body))
        response['Content-length'] = str(len(response.content))
        return response
    else:
        return HttpResponseNotAllowed(['POST'])


from empressx.empress.methods import public, private
dispatcher.register_function(public.serve, 'serve')
dispatcher.register_function(public.status, 'status')
dispatcher.register_function(private.app_info, 'private.app_info')
dispatcher.register_function(private.callback, 'private.callback')
