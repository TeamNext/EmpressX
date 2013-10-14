from empressx.retinue.tasks import web


def serve(app_name, uuid):
    web.serve.apply_async(args=(app_name, uuid))
    return True


def unserve(app_name, uuid):
    web.unserve.apply_async(args=(app_name, uuid))
    return True
