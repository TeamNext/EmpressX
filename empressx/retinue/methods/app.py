from empressx.retinue.tasks import app


def serve(app_name, uuid):
    app.serve.apply_async(args=(app_name, uuid))
    return True


def unserve(app_name, uuid):
    app.unserve.apply_async(args=(app_name, uuid))
    return True


def reserve(app_name, uuid):
    app.reserve.apply_async(args=(app_name, uuid))
    return True