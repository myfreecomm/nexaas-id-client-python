import re
import requests
from collections import namedtuple
from urllib.parse import ParseResult, urlencode, urlparse
from .oauth_token import OAuthToken

__all__ = ['NexaasIDOAuthClient']


BaseOAuthClient = namedtuple(
    'NexaasIDOAuthClient',
    'id secret scope redirect_uri server',
)


class NexaasIDOAuthClient(BaseOAuthClient):

    def __new__(cls, client_id: str, secret: str, *,
                scope: str = None, redirect_uri: str,
                server: str = None) -> BaseOAuthClient:
        server = server or 'http://localhost:3000/'
        scope = scope or 'profile'
        if not re.match(r'^[a-z]+://', server):
            server = 'https://' + server

        return super().__new__(cls, client_id, secret, scope, redirect_uri,
                               urlparse(server))

    @property
    def authorize_url(self) -> str:
        query = urlencode({
            'response_type': 'code',
            'client_id': self.id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
        })
        return self.server._replace(
            path='/oauth/authorize',
            query=query,
        ).geturl()

    def __get_oauth_token(self, **kwargs) -> OAuthToken:
        post_data = {
            'client_id': self.id,
            'client_secret': self.secret,
            'redirect_uri': self.redirect_uri,
        }
        post_data.update(kwargs)
        res = requests.post(
            self.server._replace(path='/oauth/token').geturl(),
            post_data,
        )
        res.raise_for_status()
        try:
            return OAuthToken(**res.json())

        except (ValueError, KeyError) as exc:
            new_exc = ValueError('no access token supplied')
            new_exc.__context__ = exc
            raise new_exc

    def get_token(self, code: str = None) -> OAuthToken:
        if code:
            return self.__get_oauth_token(
                grant_type='authorization_code',
                code=code,
            )
        else:
            return self.__get_oauth_token(grant_type='client_credentials')

    def refresh_token(self, token: OAuthToken) -> OAuthToken:
        return self.__get_oauth_token(
            grant_type='refresh_token',
            refresh_token=token.refresh_token,
        )
