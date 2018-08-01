from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from pw2client import PW2OAuthClient

__all__ = ['signin', 'callback']


def signin(request):
    next_url = request.GET.get('next_url') or \
               request.META.get('HTTP_REFERER')
    if next_url:
        request.session['oauth_next_url'] = next_url
    return redirect(get_client(request).authorize_url)


def callback(request):
    client = get_client(request)
    code = request.GET.get('code')
    session = request.session
    session['oauth_access_token'] = client.get_access_token(code)
    next_url = session.get('oauth_next_url')
    if next_url:
        del session['oauth_next_url']
    return redirect(next_url or '/')


def get_client(request):
    return PW2OAuthClient(
        settings.PW2_CLIENT_ID,
        settings.PW2_CLIENT_SECRET,
        server=settings.PW2_HOST,
        redirect_uri=request.build_absolute_uri(reverse(callback)),
        scope=settings.PW2_CLIENT_SCOPE,
    )
