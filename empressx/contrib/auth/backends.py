from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Group
from suds.client import Client


class TicketBackend(ModelBackend):

    def __init__(self, *args, **kwargs):
        super(TicketBackend, self).__init__(*args, **kwargs)
        self.soap_client = Client(settings.PASSPORT_SERVICE_WSDL)

    def authenticate(self, ticket=None):
        try:
            staff = self.soap_client.service.DecryptTicket(ticket)
        except:
            return None  # this may cause redirect loop

        if staff:
            try:
                user = User.objects.get(username=staff.LoginName)
            except User.DoesNotExist:
                user = User(username=staff.LoginName, is_staff=True)
                user.save()
            else:
                User.objects.filter(pk=user.pk).update(is_staff=True)

            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
