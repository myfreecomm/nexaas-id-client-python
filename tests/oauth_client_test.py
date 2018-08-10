from unittest import TestCase
from datetime import datetime
from requests.exceptions import HTTPError
from urllib.parse import parse_qs, urlparse
from ._vcr import vcr
from pw2client import PW2OAuthClient


class TestPW2OAuthClient(TestCase):

    def test_default_values(self):
        client = PW2OAuthClient('client', 'secret',
                           redirect_uri='http://localhost/callback')

        self.assertEqual(client.id, 'client')
        self.assertEqual(client.secret, 'secret')
        self.assertEqual(client.scope, 'profile')
        self.assertEqual(client.redirect_uri, 'http://localhost/callback')
        self.assertEqual(client.server.geturl(), 'http://localhost:3000/')

    def test_server_by_name(self):
        client = PW2OAuthClient('client', 'secret',
                           server='api.passaporteweb.com',
                           redirect_uri='http://localhost/callback')
        self.assertEqual(client.server.geturl(), 'https://api.passaporteweb.com')

    def test_authorize_url(self):
        client = PW2OAuthClient('client', 'secret',
                                redirect_uri='http://localhost/callback')
        url = urlparse(client.authorize_url)
        self.assertTupleEqual(
            url._replace(query=parse_qs(url.query)),
            (
                'http',
                'localhost:3000',
                '/oauth/authorize',
                '',
                {
                    'response_type': ['code'],
                    'client_id': ['client'],
                    'redirect_uri': ['http://localhost/callback'],
                    'scope': ['profile'],
                },
                '',
            ),
        )

    @vcr.use_cassette('authorized.yaml')
    def test_get_token_success(self):
        client = PW2OAuthClient('client', 'secret',
                                redirect_uri='http://localhost/callback')
        token = client.get_token('the-access-grant-code')
        self.assertEqual(token.access_token, 'some-valid-access-token')

    @vcr.use_cassette('forbidden.yaml')
    def test_get_forbidden(self):
        client = PW2OAuthClient('client', 'secret',
                                redirect_uri='http://localhost/callback')
        with self.assertRaises(HTTPError):
            client.get_token('the-access-grant-code')

    @vcr.use_cassette('empty.yaml')
    def test_get_token_empty(self):
        client = PW2OAuthClient('client', 'secret',
                                redirect_uri='http://localhost/callback')
        with self.assertRaises(ValueError):
            client.get_token('the-access-grant-code')

    @vcr.use_cassette('client-credentials.yaml')
    def test_get_client_credentials_success(self):
        client = PW2OAuthClient('client', 'secret',
                                redirect_uri='http://localhost/callback')
        token = client.get_token()
        self.assertEqual(token.access_token, 'client-credentials-access-token')

    @vcr.use_cassette('refresh-token.yaml')
    def test_refresh_token(self):
        client = PW2OAuthClient('client', 'secret',
                                redirect_uri='http://localhost/callback')
        token = client.get_token('the-access-grant-code')
        self.assertEqual(token.refresh_token, 'the-refresh-token')
        self.assertEqual(token.expires_at, datetime(2018, 8, 10, 13, 53, 53))
        self.assertEqual(token.scope, 'invite')
