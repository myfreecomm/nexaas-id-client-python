import re
import requests
from typing import NamedTuple
from urllib.parse import ParseResult, urlencode, urlparse

__all__ = ['PW2OAuthClient']


BaseOAuthClient = NamedTuple(
    'PW2OAuthClient',
    [
        ('id', str),
        ('secret', str),
        ('scope', str),
        ('redirect_uri', str),
        ('server', ParseResult),
    ],
)


class PW2OAuthClient(BaseOAuthClient):

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

    def get_access_token(self, code: str) -> str:
        res = requests.post(
            self.server._replace(path='/oauth/token').geturl(),
            {
                'client_id': self.id,
                'client_secret': self.secret,
                'redirect_uri': self.redirect_uri,
                'grant_type': 'authorization_code',
                'code': code,
            },
        )
        res.raise_for_status()
        try:
            return res.json()['access_token']

        except (ValueError, KeyError) as exc:
            new_exc = ValueError('no access token supplied')
            new_exc.__context__ = exc
            raise new_exc
