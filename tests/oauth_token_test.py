from unittest import TestCase
from unittest.mock import patch
from collections import namedtuple
from datetime import datetime
from nexaas_id_client.oauth_token import MainOAuthToken, OAuthToken, TokenSerializer


class TestOAuthToken(TestCase):

    def test_validate_oauth_token(self):
        self.assertTrue(issubclass(MainOAuthToken, OAuthToken))
        token = OAuthToken(access_token='atoken', refresh_token='rtoken')
        self.assertIsInstance(token, MainOAuthToken)
        self.assertIsInstance(token, OAuthToken)

    def test_validate_unknown_class(self):
        class MyToken:
            @property
            def access_token(self):
                return 'abc'

            @property
            def refresh_token(self):
                return None

            @property
            def expires_at(self):
                return None

            @property
            def scope(self):
                return 'profile'

        self.assertTrue(issubclass(MyToken, OAuthToken))
        token = MyToken()
        self.assertIsInstance(token, OAuthToken)

    def test_validate_named_tuple(self):
        MyToken = namedtuple(
            'MyToken', 'access_token refresh_token expires_at scope'
        )
        self.assertTrue(issubclass(MyToken, OAuthToken))
        token = MyToken('test', None, None, 'profile')
        self.assertIsInstance(token, OAuthToken)

    def test_missing_attribute(self):
        NotToken = namedtuple('NotToken', 'refresh_token other')
        self.assertFalse(issubclass(NotToken, OAuthToken))
        not_token = NotToken(None, None)
        self.assertNotIsInstance(not_token, OAuthToken)


class TestMainOAuthToken(TestCase):

    def test_default_values(self):
        token = OAuthToken(access_token='some-token')
        self.assertIsInstance(token, MainOAuthToken)
        self.assertEqual(token.access_token, 'some-token')
        self.assertIsNone(token.refresh_token)
        self.assertIsNone(token.expires_at)
        self.assertEqual(token.scope, 'profile')

    def test_refresh_token(self):
        token = OAuthToken(access_token='token1', refresh_token='token2')
        self.assertIsInstance(token, MainOAuthToken)
        self.assertEqual(token.access_token, 'token1')
        self.assertEqual(token.refresh_token, 'token2')
        self.assertIsNone(token.expires_at)
        self.assertEqual(token.scope, 'profile')

    def test_scope(self):
        token = OAuthToken(access_token='some-token', scope='invite')
        self.assertIsInstance(token, MainOAuthToken)
        self.assertEqual(token.access_token, 'some-token')
        self.assertIsNone(token.refresh_token)
        self.assertIsNone(token.expires_at)
        self.assertEqual(token.scope, 'invite')

    def test_expires_at(self):
        token = OAuthToken(
            access_token='token1',
            created_at=1533846005,
            expires_in=600,
        )
        self.assertIsInstance(token, MainOAuthToken)
        self.assertEqual(token.access_token, 'token1')
        self.assertIsNone(token.refresh_token)
        self.assertEqual(token.expires_at, datetime(2018, 8, 9, 17, 30, 5))
        self.assertEqual(token.scope, 'profile')

    def test_created_at_not_supplied(self):
        with patch('nexaas_id_client.oauth_token.datetime') as dt, \
             patch('nexaas_id_client.oauth_token._isinstance', return_value=False):
            dt.now.return_value = datetime(2018, 1, 1, 12, 0)
            token = OAuthToken(access_token='atoken', expires_in=300)
        self.assertIsInstance(token, MainOAuthToken)
        self.assertEqual(token.access_token, 'atoken')
        self.assertIsNone(token.refresh_token)
        self.assertEqual(token.expires_at, datetime(2018, 1, 1, 12, 5))
        self.assertEqual(token.scope, 'profile')


class TestTokenSerializerSerialize(TestCase):

    Token = namedtuple('Token', 'access_token refresh_token expires_at scope')

    def test_serialize_empty(self):
        token = self.Token('tk1', None, None, 'profile')
        self.assertEqual(
            set(TokenSerializer.serialize(token).split('&')),
            {
                'access_token=tk1',
                'refresh_token=',
                'expires_at=',
                'scope=profile',
            },
        )

    def test_serialize_refresh_token(self):
        token = self.Token('access-token', 'refresh-token', None, 'profile')
        self.assertEqual(
            set(TokenSerializer.serialize(token).split('&')),
            {
                'access_token=access-token',
                'refresh_token=refresh-token',
                'expires_at=',
                'scope=profile',
            },
        )

    def test_serialize_expires_at(self):
        token = self.Token('the-token', None, datetime(2100, 10, 10, 10, 10), 'profile')
        self.assertEqual(
            set(TokenSerializer.serialize(token).split('&')),
            {
                'access_token=the-token',
                'refresh_token=',
                'expires_at=2100-10-10+10%3A10%3A00',
                'scope=profile',
            },
        )

    def test_full_serialization(self):
        token = self.Token('access-token', 'refresh-token', datetime(1970, 1, 1), 'profile')
        self.assertEqual(
            set(TokenSerializer.serialize(token).split('&')),
            {
                'access_token=access-token',
                'refresh_token=refresh-token',
                'expires_at=1970-01-01+00%3A00%3A00',
                'scope=profile',
            },
        )


class TestTokenSerializerDeserialize(TestCase):

    def test_deserialize_empty(self):
        token = TokenSerializer.deserialize(
            'access_token=tk1&refresh_token=&expires_at=&scope=profile'
        )
        self.assertEqual(token.access_token, 'tk1')
        self.assertIsNone(token.refresh_token)
        self.assertIsNone(token.expires_at)

    def test_deserialize_refresh_token(self):
        token = TokenSerializer.deserialize(
            'access_token=access-token&'
            'refresh_token=refresh-token&'
            'expires_at=&'
            'scope=profile'
        )
        self.assertEqual(token.access_token, 'access-token')
        self.assertEqual(token.refresh_token, 'refresh-token')
        self.assertIsNone(token.expires_at)

    def test_serialize_expires_at(self):
        token = TokenSerializer.deserialize(
            'access_token=the-token&'
            'refresh_token=&'
            'expires_at=2100-10-10+10%3A10%3A00&'
            'scope=profile'
        )
        self.assertEqual(token.access_token, 'the-token')
        self.assertIsNone(token.refresh_token)
        self.assertEqual(token.expires_at, datetime(2100, 10, 10, 10, 10))

    def test_full_serialization(self):
        token = TokenSerializer.deserialize(
            'access_token=access-token&'
            'refresh_token=refresh-token&'
            'expires_at=1970-01-01+00%3A00%3A00&'
            'scope=profile'
        )
        self.assertEqual(token.access_token, 'access-token')
        self.assertEqual(token.refresh_token, 'refresh-token')
        self.assertEqual(token.expires_at, datetime(1970, 1, 1))
