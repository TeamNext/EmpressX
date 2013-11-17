import urllib

from django.conf import settings
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect

from .forms import AuthenticationForm


def login(request):

    if request.method == 'GET':
        location = request.GET.get('next')
        location = location if location else settings.LOGIN_REDIRECT_URL

        if request.user.is_authenticated():
            return HttpResponseRedirect(location)

        form = AuthenticationForm(request.GET)
        if form.is_valid():
            user = auth.authenticate(ticket=form.cleaned_data['ticket'])
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(location)

        return HttpResponseRedirect(settings.PASSPORT_SERVICE_SIGNIN_URL +
            '?url=' + urllib.quote(request.build_absolute_uri()))
    else:
        raise Http404()


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(settings.PASSPORT_SERVICE_SIGNOUT_URL +
        '?url=' + request.build_absolute_uri(reverse('accounts:login')))
