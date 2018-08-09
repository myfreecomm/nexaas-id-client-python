from unittest import TestCase
from unittest.mock import patch
from collections import namedtuple
from datetime import datetime
from pw2client.oauth_token import AbstractToken, OAuthToken, TokenSerializer


class TestAbstractToken(TestCase):

    def test_validate_oauth_token(self):
        self.assertTrue(issubclass(OAuthToken, AbstractToken))
        token = OAuthToken('test-token')
        self.assertIsInstance(token, AbstractToken)

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

        self.assertTrue(issubclass(MyToken, AbstractToken))
        token = MyToken()
        self.assertIsInstance(token, AbstractToken)

    def test_validate_named_tuple(self):
        MyToken = namedtuple('MyToken', 'access_token refresh_token expires_at')
        self.assertTrue(issubclass(MyToken, AbstractToken))
        token = MyToken('test', None, None)
        self.assertIsInstance(token, AbstractToken)

    def test_missing_attribute(self):
        NotToken = namedtuple('NotToken', 'refresh_token other')
        self.assertFalse(issubclass(NotToken, AbstractToken))
        not_token = NotToken(None, None)
        self.assertNotIsInstance(not_token, AbstractToken)


class TestOAuthToken(TestCase):

    def test_default_values(self):
        token = OAuthToken(access_token='some-token')
        self.assertEqual(token.access_token, 'some-token')
        self.assertIsNone(token.refresh_token)
        self.assertIsNone(token.expires_at)

    def test_refresh_token(self):
        token = OAuthToken(access_token='token1', refresh_token='token2')
        self.assertEqual(token.access_token, 'token1')
        self.assertEqual(token.refresh_token, 'token2')
        self.assertIsNone(token.expires_at)

    def test_expires_at(self):
        token = OAuthToken(access_token='token1', expires_at=1533846605)
        self.assertEqual(token.access_token, 'token1')
        self.assertIsNone(token.refresh_token)
        self.assertEqual(token.expires_at, datetime(2018, 8, 9, 17, 30, 5))

    @patch('datetime.datetime.now', return_value=datetime(2018, 1, 1, 12, 0))
    def test_expires_in(self, _now):
        token = OAuthToken(access_token='atoken', expires_in=300)
        self.assertEqual(token.access_token, 'atoken')
        self.assertIsNone(token.refresh_token)
        self.assertEqual(token.expires_at, datetime(2018, 1, 1, 12, 5))


class TestTokenSerializerSerialize(TestCase):

    Token = namedtuple('Token', 'access_token refresh_token expires_at')

    def test_serialize_empty(self):
        token = self.Token('tk1', None, None)
        self.assertEqual(
            TokenSerializer.serialize(token),
            'access_token=tk1&refresh_token=&expires_at=',
        )

    def test_serialize_refresh_token(self):
        token = self.Token('access-token', 'refresh-token', None)
        self.assertEqual(
            TokenSerializer.serialize(token),
            'access_token=access-token&'
            'refresh_token=refresh-token&'
            'expires_at=',
        )

    def test_serialize_expires_at(self):
        token = self.Token('the-token', None, datetime(2100, 10, 10, 10, 10))
        self.assertEqual(
            TokenSerializer.serialize(token),
            'access_token=the-token&'
            'refresh_token=&'
            'expires_at=2100-10-10+10%3A10%3A00',
        )

    def test_full_serialization(self):
        token = self.Token('access-token', 'refresh-token', datetime(1970, 1, 1))
        self.assertEqual(
            TokenSerializer.serialize(token),
            'access_token=access-token&'
            'refresh_token=refresh-token&'
            'expires_at=1970-01-01+00%3A00%3A00',
        )


class TestTokenSerializerDeserialize(TestCase):

    def test_deserialize_empty(self):
        token = TokenSerializer.deserialize(
            'access_token=tk1&refresh_token=&expires_at='
        )
        self.assertEqual(token.access_token, 'tk1')
        self.assertIsNone(token.refresh_token)
        self.assertIsNone(token.expires_at)

    def test_deserialize_refresh_token(self):
        token = TokenSerializer.deserialize(
            'access_token=access-token&'
            'refresh_token=refresh-token&'
            'expires_at='
        )
        self.assertEqual(token.access_token, 'access-token')
        self.assertEqual(token.refresh_token, 'refresh-token')
        self.assertIsNone(token.expires_at)

    def test_serialize_expires_at(self):
        token = TokenSerializer.deserialize(
            'access_token=the-token&'
            'refresh_token=&'
            'expires_at=2100-10-10+10%3A10%3A00'
        )
        self.assertEqual(token.access_token, 'the-token')
        self.assertIsNone(token.refresh_token)
        self.assertEqual(token.expires_at, datetime(2100, 10, 10, 10, 10))

    def test_full_serialization(self):
        token = TokenSerializer.deserialize(
            'access_token=access-token&'
            'refresh_token=refresh-token&'
            'expires_at=1970-01-01+00%3A00%3A00'
        )
        self.assertEqual(token.access_token, 'access-token')
        self.assertEqual(token.refresh_token, 'refresh-token')
        self.assertEqual(token.expires_at, datetime(1970, 1, 1))
