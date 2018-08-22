from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from nexaas_id_client import NexaasIDOAuthClient
from nexaas_id_client.oauth_token import TokenSerializer

__all__ = ['signin', 'callback']


def signin(request):
    next_url = request.GET.get('next_url') or \
               request.META.get('HTTP_REFERER')
    if next_url:
        request.session['oauth_next_url'] = next_url
    return redirect(get_client(request).authorize_url)


def signout(request):
    session = request.session
    if 'oauth_token' in session:
        del session['oauth_token']
    next_url = request.GET.get('next_url') or \
               session.get('oauth_next_url') or \
               request.META.get('HTTP_REFERER') or \
               '/'
    return redirect(next_url)


def callback(request):
    client = get_client(request)
    code = request.GET.get('code')
    session = request.session
    session['oauth_token'] = TokenSerializer.serialize(client.get_token(code))
    next_url = session.get('oauth_next_url')
    if next_url:
        del session['oauth_next_url']
    return redirect(next_url or '/')


def get_client(request):
    return NexaasIDOAuthClient(
        settings.NEXAAS_ID_CLIENT_ID,
        settings.NEXAAS_ID_CLIENT_SECRET,
        server=settings.NEXAAS_ID_HOST,
        redirect_uri=request.build_absolute_uri(reverse(callback)),
        scope=settings.NEXAAS_ID_CLIENT_SCOPE,
    )
