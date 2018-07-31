from functools import wraps
import inspect
from flask import Blueprint, current_app, redirect, request, session, url_for
from ..oauth_client import PW2OAuthClient

__all__ = ['authorization_required', 'oauth']


oauth = Blueprint('pw2_oauth', __name__)


def authorization_required(wrapped):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        if 'oauth_access_token' not in session:
            return redirect(url_for('pw2_oauth.signin'))
        if 'access_token' in inspect.signature(wrapped).parameters:
            kwargs['access_token'] = session['oauth_access_token']
        return wrapped(*args, **kwargs)
    return wrapper


@oauth.route('/signin')
def signin():
    next_url = request.args.get('next_url') or \
               request.headers.get('Referer')
    if next_url:
        session['oauth_next_url'] = next_url
    return redirect(get_client().authorize_url)


@oauth.route('/callback')
def callback():
    client = get_client()
    code = request.args.get('code')
    session['oauth_access_token'] = client.get_access_token(code)
    next_url = session.get('oauth_next_url')
    if next_url:
        del session['oauth_next_url']
    return redirect(next_url or '/')


def get_client():
    return PW2OAuthClient(
        current_app.config['PW2_CLIENT_ID'],
        current_app.config['PW2_CLIENT_SECRET'],
        server=current_app.config.get('PW2_HOST'),
        redirect_uri=url_for('pw2_oauth.callback', _external=True),
        scope=current_app.config.get('PW2_CLIENT_SCOPE'),
    )
