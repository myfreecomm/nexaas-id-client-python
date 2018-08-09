from abc import ABCMeta
from collections import namedtuple
from datetime import datetime, timedelta
from typing import Union
from urllib.parse import parse_qsl, urlencode

__all__ = ['OAuthToken', 'TokenSerializer']


class OAuthToken(metaclass=ABCMeta):

    Base = namedtuple(
        'OAuthToken',
        'access_token refresh_token expires_at',
    )

    @classmethod
    def __subclasshook__(cls, C):
        for attr in cls.Base._fields:
            if not any(attr in B.__dict__ for B in C.__mro__):
                return NotImplemented
        return True

    @staticmethod
    def build(*args, **kwargs) -> Base:
        return MainOAuthToken(*args, **kwargs)


class MainOAuthToken(OAuthToken.Base):

    def __new__(cls, access_token: str, refresh_token: str = None,
                expires_at: Union[int, datetime] = -1,
                expires_in: int = -1, **__) -> OAuthToken.Base:
        if not isinstance(expires_at, datetime):
            if expires_at >= 0:
                expires_at = datetime.fromtimestamp(expires_at)
            elif expires_in >= 0:
                expires_at = datetime.now() + timedelta(seconds=expires_in)
            else:
                expires_at = None
        return super().__new__(cls, access_token, refresh_token, expires_at)

    @property
    def expired(self) -> bool:
        return self.expires_at < datetime.now()

OAuthToken.register(MainOAuthToken)


class TokenSerializer:

    @staticmethod
    def serialize(token: OAuthToken) -> str:
        return urlencode({
            attr: getattr(token, attr) or ''
            for attr in OAuthToken.Base._fields
        })

    @staticmethod
    def deserialize(token: str) -> OAuthToken:
        resource = {
            attr: value or None
            for attr, value in parse_qsl(token)
            if attr in OAuthToken.Base._fields
        }

        if resource.get('expires_at'):
            resource['expires_at'] = datetime.strptime(
                resource['expires_at'],
                r'%Y-%m-%d %H:%M:%S',
            )
        return OAuthToken.build(**resource)
