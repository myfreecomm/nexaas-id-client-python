from functools import wraps
import inspect
from django.shortcuts import redirect
from django.urls import reverse
from pw2client import PW2Client
from . import views

__all__ = ['authorization_required']


def authorization_required(wrapped):
    @wraps(wrapped)
    def wrapper(request, *args, **kwargs):
        session = request.session
        if 'oauth_access_token' not in session:
            return redirect(reverse(views.signin))
        kwargs['api_client'] = PW2Client.from_oauth(
            session['oauth_access_token'],
            client=views.get_client(request),
        )
        return wrapped(request, *args, **kwargs)
    return wrapper
