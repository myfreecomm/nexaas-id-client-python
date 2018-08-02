from unittest import TestCase, skip
from requests.exceptions import HTTPError
from urllib.parse import parse_qs, urlparse
from ._vcr import vcr
from pw2client import PW2Client, PW2OAuthClient


class TestPW2Client(TestCase):
    @staticmethod
    def build_oauth_client():
        return PW2OAuthClient('client', 'secret',
                              redirect_uri='http://localhost/callback')

    def test_tuple_attributes(self):
        client = PW2Client.from_oauth(
            'the-access-token',
            client=self.build_oauth_client(),
        )
        self.assertEqual(client.access_token, 'the-access-token')
        self.assertEqual(client.id, 'client')
        self.assertEqual(client.secret, 'secret')
        self.assertEqual(client.server.netloc, 'localhost:3000')
        self.assertEqual(client.server.path, '/')
        self.assertEqual(
            client.navbar_url,
            'http://localhost:3000/api/v1/widgets/navbar.js?'
            'access_token=the-access-token',
        )

    @skip('TODO: build cassette')
    def test_personal_info(self):
        raise NotImplementedError

    @skip('TODO: build cassette')
    def test_professional_info(self):
        raise NotImplementedError

    @skip('TODO: build cassette')
    def test_emails(self):
        raise NotImplementedError

    @skip('TODO: build cassette')
    def test_contacts(self):
        raise NotImplementedError
