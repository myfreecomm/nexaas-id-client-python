from functools import wraps
import inspect
from django.shortcuts import redirect
from django.urls import reverse
from . import views

__all__ = ['authorization_required']


def authorization_required(wrapped):
    @wraps(wrapped)
    def wrapper(request, *args, **kwargs):
        session = request.session
        if 'oauth_access_token' not in session:
            return redirect(reverse(views.signin))
        if 'access_token' in inspect.signature(wrapped).parameters:
            kwargs['access_token'] = session['oauth_access_token']
        return wrapped(request, *args, **kwargs)
    return wrapper
