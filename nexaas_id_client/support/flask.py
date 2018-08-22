from functools import wraps
import inspect
from flask import Blueprint, current_app, redirect, request, session, url_for
from nexaas_id_client import NexaasIDClient, NexaasIDOAuthClient
from nexaas_id_client.oauth_token import OAuthToken, TokenSerializer

__all__ = ['authorization_required', 'oauth']


oauth = Blueprint('nexaas_id_oauth', __name__)


def authorization_required(wrapped):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        if 'oauth_token' not in session:
            return redirect(url_for('nexaas_id_oauth.signin'))
        kwargs['api_client'] = NexaasIDClient.from_oauth(
            TokenSerializer.deserialize(session['oauth_token']),
            client=get_client(),
        )
        return wrapped(*args, **kwargs)
    return wrapper


@oauth.route('/signin')
def signin():
    next_url = request.args.get('next_url') or \
               request.headers.get('Referer')
    if next_url:
        session['oauth_next_url'] = next_url
    return redirect(get_client().authorize_url)


@oauth.route('/signout')
def signout():
    if 'oauth_token' in session:
        del session['oauth_token']
    next_url = request.args.get('next_url') or \
               session.get('oauth_next_url') or \
               request.headers.get('Referer') or \
               '/'
    return redirect(next_url)


@oauth.route('/callback')
def callback():
    client = get_client()
    code = request.args.get('code')
    session['oauth_token'] = TokenSerializer.serialize(client.get_token(code))
    next_url = session.get('oauth_next_url')
    if next_url:
        del session['oauth_next_url']
    return redirect(next_url or '/')


def get_client():
    return NexaasIDOAuthClient(
        current_app.config['NEXAAS_ID_CLIENT_ID'],
        current_app.config['NEXAAS_ID_CLIENT_SECRET'],
        server=current_app.config.get('NEXAAS_ID_HOST'),
        redirect_uri=url_for('nexaas_id_oauth.callback', _external=True),
        scope=current_app.config.get('NEXAAS_ID_CLIENT_SCOPE'),
    )
