from functools import wraps
import inspect
from django.shortcuts import redirect
from django.urls import reverse
from nexaas_id_client import NexaasIDClient
from nexaas_id_client.oauth_token import TokenSerializer
from nexaas_id_client.helpers import signed_in
from . import views

__all__ = ['authorization_required']


def authorization_required(wrapped):
    """
    XXX: [side effect] Redirect to sign out if the view returns falsy
    FIXME: change this behavior
    """
    @wraps(wrapped)
    def wrapper(request, *args, **kwargs):
        session = get_session(request)
        if not session:
            return redirect(reverse(views.signin))
        kwargs['api_client'] = get_api_client(request, session)
        return deal_with_request(wrapped, request, args, kwargs)
    return wrapper


def get_session(request):
    session = request.session
    return session if 'oauth_token' in session else None


def get_api_client(request, session):
    return NexaasIDClient.from_oauth(
        TokenSerializer.deserialize(session['oauth_token']),
        client=views.get_client(request),
    )


def deal_with_request(wrapped, request, args, kwargs):
    response = None
    with signed_in() as unsigned:
        response = wrapped(request, *args, **kwargs)
    return response or unsigned.redirect
